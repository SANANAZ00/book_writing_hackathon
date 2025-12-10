import openai
from typing import Dict, Any, Optional
from app.agents.base import BaseSubagent, SubagentConfig, SubagentResult

class ContentExpansionSubagent(BaseSubagent):
    """Subagent for content expansion and enhancement"""

    def __init__(self):
        config = SubagentConfig(
            name="Content Expansion Agent",
            description="Specializes in expanding and enhancing content with examples, explanations, and context",
            capabilities=[
                "content expansion",
                "example generation",
                "explanation enhancement",
                "context addition",
                "content consistency",
                "educational improvement"
            ]
        )
        super().__init__(config)

    async def _process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> SubagentResult:
        """
        Process content expansion tasks
        """
        system_prompt = self._build_system_prompt(task, context)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

            result_content = response.choices[0].message.content

            # Structure the expanded content
            expanded_content = self._structure_content(result_content)

            return SubagentResult(
                success=True,
                data={
                    "expanded_content": expanded_content,
                    "original_task": task
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SubagentResult(
                success=False,
                message=f"Error processing content expansion task: {str(e)}"
            )

    def _structure_content(self, content: str) -> Dict[str, Any]:
        """
        Structure the expanded content into sections
        """
        return {
            "content": content,
            "sections_added": ["examples", "explanations", "context"],
            "quality_score": 0.8  # Would be calculated based on analysis
        }