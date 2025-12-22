"""
Utility module for managing LLM clients (OpenAI and Cohere)
"""
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

import openai
from app.config import settings

logger = logging.getLogger(__name__)

# Import cohere only when needed to handle cases where it might not be installed
def get_cohere_client():
    """Lazy load and return Cohere client"""
    try:
        import cohere
        logger.debug("Initializing Cohere client")
        client = cohere.AsyncClient(
            api_key=settings.COHERE_API_KEY,
            base_url=settings.COHERE_BASE_URL
        )
        logger.info("Cohere client initialized successfully")
        return client
    except ImportError:
        logger.error("Cohere package not found. Install with: pip install cohere")
        raise ImportError("cohere package is required for Cohere models. Install with: pip install cohere")


def get_openai_client():
    """Return OpenAI client"""
    logger.debug("Initializing OpenAI client")
    client = openai.AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL
    )
    logger.info("OpenAI client initialized successfully")
    return client


class ModelInfo(BaseModel):
    provider: str
    model: str
    max_tokens: int = 4096
    supports_streaming: bool = True


class LLMManager:
    """Manager for handling multiple LLM providers"""
    
    def __init__(self):
        self._validate_configured_models()
        
    def _validate_configured_models(self):
        """Validate that configured models are in available models list"""
        if settings.DEFAULT_PROVIDER not in settings.AVAILABLE_MODELS:
            raise ValueError(f"Default provider {settings.DEFAULT_PROVIDER} not in available models")
            
        if settings.DEFAULT_MODEL not in settings.AVAILABLE_MODELS.get(settings.DEFAULT_PROVIDER, []):
            raise ValueError(f"Default model {settings.DEFAULT_MODEL} not in available models for provider {settings.DEFAULT_PROVIDER}")
        
        logger.info(f"LLM Manager initialized with default: {settings.DEFAULT_PROVIDER}/{settings.DEFAULT_MODEL}")
    
    def validate_provider_and_model(self, provider: str, model: str) -> bool:
        """Validate if a provider and model combination is supported"""
        if provider not in settings.AVAILABLE_MODELS:
            return False
        
        if model not in settings.AVAILABLE_MODELS[provider]:
            return False
            
        return True
    
    def get_model_info(self, provider: str, model: str) -> ModelInfo:
        """Get model information"""
        if not self.validate_provider_and_model(provider, model):
            raise ValueError(f"Invalid provider/model combination: {provider}/{model}")
        
        # Set max tokens based on provider/model
        max_tokens_map = {
            "openai": {
                "gpt-4o-mini": 128000,
                "gpt-4o": 128000
            },
            "cohere": {
                "command-r": 128000,
                "command-r-plus": 128000
            }
        }
        
        max_tokens = max_tokens_map.get(provider, {}).get(model, 4096)
        
        return ModelInfo(
            provider=provider,
            model=model,
            max_tokens=max_tokens
        )
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        provider: str = settings.DEFAULT_PROVIDER,
        model: str = settings.DEFAULT_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using specified LLM provider and model
        
        Args:
            messages: List of message dictionaries with role and content
            provider: LLM provider ('openai' or 'cohere')
            model: Specific model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Dictionary containing response text, usage info, and model info
        """
        logger.info(f"Generating response using provider: {provider}, model: {model}")
        
        if not self.validate_provider_and_model(provider, model):
            raise ValueError(f"Unsupported provider/model combination: {provider}/{model}")
        
        try:
            if provider == "openai":
                return await self._generate_with_openai(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                    **kwargs
                )
            elif provider == "cohere":
                return await self._generate_with_cohere(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
            else:
                raise ValueError(f"Unsupported provider: {provider}")
                
        except Exception as e:
            logger.error(f"Error generating response with {provider}/{model}: {str(e)}")
            raise
    
    async def _generate_with_openai(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        client = get_openai_client()
        
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Extract the response content
            content = response.choices[0].message.content
            usage = response.usage
            
            return {
                "response": content,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens if usage else 0,
                    "completion_tokens": usage.completion_tokens if usage else 0,
                    "total_tokens": usage.total_tokens if usage else 0
                },
                "model_used": model,
                "provider": "openai"
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def _generate_with_cohere(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Cohere"""
        client = get_cohere_client()
        
        # Convert messages to Cohere format
        # For conversation-style generation, we'll concatenate messages
        message_text = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                message_text += f"System: {content}\n\n"
            elif role == "user":
                message_text += f"User: {content}\n\n"
            elif role == "assistant":
                message_text += f"Assistant: {content}\n\n"
        
        # Remove trailing newline
        message_text = message_text.rstrip("\n ")
        
        try:
            response = await client.chat(
                model=model,
                message=message_text,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            content = response.text
            usage = response.meta if hasattr(response, 'meta') else None
            
            return {
                "response": content,
                "usage": {
                    "input_tokens": getattr(getattr(usage, 'tokens', None), 'input_tokens', 0) if usage else 0,
                    "output_tokens": getattr(getattr(usage, 'tokens', None), 'output_tokens', 0) if usage else 0,
                },
                "model_used": model,
                "provider": "cohere"
            }
            
        except Exception as e:
            logger.error(f"Cohere API error: {str(e)}")
            raise
    
    async def embed_texts(self, texts: List[str], input_type: str = "search_document") -> List[List[float]]:
        """
        Generate embeddings for texts using Cohere embeddings

        Args:
            texts: List of texts to embed
            input_type: Type of input - "search_document" for documents, "search_query" for queries
        """
        client = get_cohere_client()

        try:
            response = await client.embed(
                texts=texts,
                model=settings.EMBEDDING_MODEL,
                input_type=input_type
            )

            embeddings = response.embeddings
            return embeddings

        except Exception as e:
            logger.error(f"Embedding generation error: {str(e)}")
            raise