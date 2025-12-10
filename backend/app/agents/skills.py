import abc
import logging
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel
import openai
from app.config import settings

logger = logging.getLogger(__name__)

class SkillConfig(BaseModel):
    """Configuration for a skill"""
    name: str
    description: str
    parameters: Dict[str, Any]
    required_params: List[str]

class SkillResult(BaseModel):
    """Result from a skill execution"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseSkill(abc.ABC):
    """Base class for all skills"""

    def __init__(self, config: SkillConfig):
        self.config = config
        openai.api_key = settings.OPENAI_API_KEY
        self.name = config.name
        self.description = config.description
        self.parameters = config.parameters
        self.required_params = config.required_params

    async def execute(self, **kwargs) -> SkillResult:
        """
        Execute the skill with provided parameters
        """
        try:
            logger.info(f"Skill {self.name} executing with parameters: {list(kwargs.keys())}")

            # Validate required parameters
            missing_params = []
            for param in self.required_params:
                if param not in kwargs:
                    missing_params.append(param)

            if missing_params:
                return SkillResult(
                    success=False,
                    message=f"Missing required parameters: {missing_params}"
                )

            # Validate parameter types/values if specified
            validation_result = self._validate_parameters(kwargs)
            if not validation_result.success:
                return validation_result

            # Execute the specific skill
            result = await self._execute_skill(**kwargs)

            return result

        except Exception as e:
            logger.error(f"Error in skill {self.name}: {str(e)}")
            return SkillResult(
                success=False,
                message=f"Error in skill {self.name}: {str(e)}"
            )

    def _validate_parameters(self, params: Dict[str, Any]) -> SkillResult:
        """
        Validate parameters before execution
        """
        # Default validation - check types if specified in config
        for param_name, param_value in params.items():
            if param_name in self.parameters:
                expected_type = self.parameters[param_name].get('type')
                if expected_type and not isinstance(param_value, expected_type):
                    return SkillResult(
                        success=False,
                        message=f"Parameter {param_name} should be of type {expected_type}, got {type(param_value)}"
                    )

        return SkillResult(success=True)

    @abc.abstractmethod
    async def _execute_skill(self, **kwargs) -> SkillResult:
        """
        Execute the specific skill - to be implemented by subclasses
        """
        pass

    def _build_system_prompt(self, **kwargs) -> str:
        """
        Build system prompt for the skill
        """
        base_prompt = f"""
        You are executing the skill: {self.name}
        Description: {self.description}

        Parameters provided: {kwargs}

        Perform the requested action and provide a helpful, accurate response.
        """

        return base_prompt

# Skill implementations
class ExplainConceptSkill(BaseSkill):
    """Skill to explain concepts in simple terms"""

    def __init__(self):
        config = SkillConfig(
            name="Explain Concept in Simple Terms",
            description="Explains complex concepts in simple, understandable terms with analogies",
            parameters={
                "concept": {"type": str, "description": "The concept to explain"},
                "target_audience": {"type": str, "description": "Target audience level (beginner, intermediate, advanced)"},
                "examples": {"type": bool, "description": "Whether to include examples"}
            },
            required_params=["concept"]
        )
        super().__init__(config)

    async def _execute_skill(self, **kwargs) -> SkillResult:
        concept = kwargs.get('concept')
        target_audience = kwargs.get('target_audience', 'beginner')
        include_examples = kwargs.get('examples', True)

        system_prompt = self._build_system_prompt(**kwargs)

        user_message = f"""
        Explain the concept of '{concept}' to a {target_audience} level audience.
        Use simple language, analogies, and clear explanations.
        Include practical examples if requested.
        Structure the explanation with:
        1. Simple definition
        2. Analogy or real-world comparison
        3. Key points to remember
        4. Practical application
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,
                max_tokens=600
            )

            explanation = response.choices[0].message.content

            return SkillResult(
                success=True,
                data={
                    "explanation": explanation,
                    "concept": concept,
                    "target_audience": target_audience
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error explaining concept: {str(e)}"
            )

class RewriteInBookToneSkill(BaseSkill):
    """Skill to rewrite content in the book's tone"""

    def __init__(self):
        config = SkillConfig(
            name="Rewrite in Book Tone",
            description="Rewrites content to match the book's educational and professional tone",
            parameters={
                "content": {"type": str, "description": "Content to rewrite"},
                "tone_style": {"type": str, "description": "Style to match (educational, professional, etc.)"}
            },
            required_params=["content"]
        )
        super().__init__(config)

    async def _execute_skill(self, **kwargs) -> SkillResult:
        content = kwargs.get('content')
        tone_style = kwargs.get('tone_style', 'educational')

        system_prompt = self._build_system_prompt(**kwargs)

        user_message = f"""
        Rewrite the following content to match a {tone_style} tone appropriate for an educational book:
        {content}

        Maintain the core meaning but adjust the language, structure, and style to be:
        - Educational and informative
        - Professional yet approachable
        - Clear and concise
        - Consistent with academic writing standards
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.4,
                max_tokens=800
            )

            rewritten_content = response.choices[0].message.content

            return SkillResult(
                success=True,
                data={
                    "original_content": content,
                    "rewritten_content": rewritten_content,
                    "tone_style": tone_style
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error rewriting content: {str(e)}"
            )

class GenerateUIComponentSkill(BaseSkill):
    """Skill to generate UI components"""

    def __init__(self):
        config = SkillConfig(
            name="Generate UI Component",
            description="Generates UI component code based on requirements",
            parameters={
                "component_type": {"type": str, "description": "Type of component (button, card, form, etc.)"},
                "requirements": {"type": str, "description": "Component requirements and features"},
                "framework": {"type": str, "description": "Target framework (React, Vue, etc.)"}
            },
            required_params=["component_type", "requirements"]
        )
        super().__init__(config)

    async def _execute_skill(self, **kwargs) -> SkillResult:
        component_type = kwargs.get('component_type')
        requirements = kwargs.get('requirements')
        framework = kwargs.get('framework', 'React')

        system_prompt = self._build_system_prompt(**kwargs)

        user_message = f"""
        Generate a {framework} UI component for a {component_type} with the following requirements:
        {requirements}

        Include:
        - Proper component structure
        - Accessibility features
        - Responsive design
        - Clean, maintainable code
        - Proper TypeScript/JavaScript typing if applicable
        - Documentation comments
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            component_code = response.choices[0].message.content

            return SkillResult(
                success=True,
                data={
                    "component_type": component_type,
                    "requirements": requirements,
                    "component_code": component_code,
                    "framework": framework
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error generating UI component: {str(e)}"
            )

class GenerateAPIRouteSkill(BaseSkill):
    """Skill to generate API route code"""

    def __init__(self):
        config = SkillConfig(
            name="Generate API Route",
            description="Generates API route code with proper validation and error handling",
            parameters={
                "route_purpose": {"type": str, "description": "Purpose of the API route"},
                "method": {"type": str, "description": "HTTP method (GET, POST, PUT, DELETE)"},
                "parameters": {"type": str, "description": "Expected parameters"},
                "response_format": {"type": str, "description": "Expected response format"}
            },
            required_params=["route_purpose", "method"]
        )
        super().__init__(config)

    async def _execute_skill(self, **kwargs) -> SkillResult:
        route_purpose = kwargs.get('route_purpose')
        method = kwargs.get('method', 'GET')
        parameters = kwargs.get('parameters', '')
        response_format = kwargs.get('response_format', 'JSON')

        system_prompt = self._build_system_prompt(**kwargs)

        user_message = f"""
        Generate an API route for: {route_purpose}
        HTTP Method: {method}
        Parameters: {parameters}
        Response Format: {response_format}

        Include:
        - Proper request validation
        - Error handling
        - Response formatting
        - Security considerations
        - Documentation
        - Type hints where appropriate
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=800
            )

            route_code = response.choices[0].message.content

            return SkillResult(
                success=True,
                data={
                    "route_purpose": route_purpose,
                    "method": method,
                    "parameters": parameters,
                    "response_format": response_format,
                    "route_code": route_code
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error generating API route: {str(e)}"
            )

class OptimizeEmbeddingChunkSkill(BaseSkill):
    """Skill to optimize embedding chunks for RAG"""

    def __init__(self):
        config = SkillConfig(
            name="Optimize Embedding Chunk",
            description="Optimizes text chunks for better embedding and retrieval in RAG systems",
            parameters={
                "text": {"type": str, "description": "Text to optimize"},
                "max_chunk_size": {"type": int, "description": "Maximum chunk size in tokens"},
                "overlap": {"type": int, "description": "Overlap between chunks in tokens"}
            },
            required_params=["text"]
        )
        super().__init__(config)

    async def _execute_skill(self, **kwargs) -> SkillResult:
        text = kwargs.get('text')
        max_chunk_size = kwargs.get('max_chunk_size', 500)
        overlap = kwargs.get('overlap', 50)

        system_prompt = self._build_system_prompt(**kwargs)

        user_message = f"""
        Optimize the following text for embedding in a RAG system:
        {text}

        Requirements:
        - Chunk size should not exceed {max_chunk_size} tokens
        - Maintain semantic coherence within chunks
        - Include {overlap} tokens of overlap between chunks
        - Preserve important context and relationships
        - Ensure chunks are suitable for semantic search

        Provide optimized chunks and recommendations for the chunking strategy.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.4,
                max_tokens=800
            )

            optimization_result = response.choices[0].message.content

            return SkillResult(
                success=True,
                data={
                    "original_text": text,
                    "optimized_result": optimization_result,
                    "max_chunk_size": max_chunk_size,
                    "overlap": overlap
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error optimizing embedding chunk: {str(e)}"
            )

class ImproveRetrievalQualitySkill(BaseSkill):
    """Skill to improve retrieval quality in RAG systems"""

    def __init__(self):
        config = SkillConfig(
            name="Improve Retrieval Quality",
            description="Improves the quality of retrieval in RAG systems through query optimization and strategy",
            parameters={
                "query": {"type": str, "description": "Original query"},
                "context": {"type": str, "description": "Additional context if available"},
                "strategy": {"type": str, "description": "Improvement strategy to use"}
            },
            required_params=["query"]
        )
        super().__init__(config)

    async def _execute_skill(self, **kwargs) -> SkillResult:
        query = kwargs.get('query')
        context = kwargs.get('context', '')
        strategy = kwargs.get('strategy', 'query_expansion')

        system_prompt = self._build_system_prompt(**kwargs)

        user_message = f"""
        Improve the following query for better retrieval in a RAG system:
        Query: {query}
        Context: {context}
        Strategy: {strategy}

        Provide:
        - Optimized query
        - Query expansion terms if applicable
        - Suggested search parameters
        - Quality improvement recommendations
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,
                max_tokens=600
            )

            improvement_result = response.choices[0].message.content

            return SkillResult(
                success=True,
                data={
                    "original_query": query,
                    "improved_result": improvement_result,
                    "strategy": strategy
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Error improving retrieval quality: {str(e)}"
            )