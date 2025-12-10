import openai
from typing import Dict, Any, Optional
from app.agents.base import BaseSubagent, SubagentConfig, SubagentResult

class DeploymentHelperSubagent(BaseSubagent):
    """Subagent for deployment and CI/CD assistance"""

    def __init__(self):
        config = SubagentConfig(
            name="Deployment/CI Helper Agent",
            description="Specializes in deployment processes, CI/CD pipelines, and operational tasks",
            capabilities=[
                "deployment processes",
                "CI/CD pipeline",
                "monitoring setup",
                "environment configuration",
                "build optimization",
                "release management"
            ]
        )
        super().__init__(config)

    async def _process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> SubagentResult:
        """
        Process deployment and CI/CD tasks
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

            # Extract deployment recommendations
            recommendations = self._extract_deployment_recommendations(result_content)

            return SubagentResult(
                success=True,
                data={
                    "recommendations": recommendations,
                    "instructions": result_content
                },
                metadata={
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model_used": "gpt-4"
                }
            )

        except Exception as e:
            return SubagentResult(
                success=False,
                message=f"Error processing deployment task: {str(e)}"
            )

    def _extract_deployment_recommendations(self, content: str) -> Dict[str, Any]:
        """
        Extract structured deployment recommendations
        """
        return {
            "configuration": ["environment variables", "security settings"],
            "pipeline": ["build steps", "test procedures", "deployment steps"],
            "monitoring": ["health checks", "logging setup", "alerting"],
            "best_practices": content
        }