import abc
import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import openai
from app.config import settings

logger = logging.getLogger(__name__)

class SubagentConfig(BaseModel):
    """Configuration for a subagent"""
    name: str
    description: str
    capabilities: List[str]
    temperature: float = 0.7
    max_tokens: int = 500

class SubagentResult(BaseModel):
    """Result from a subagent operation"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseSubagent(abc.ABC):
    """Base class for all subagents"""

    def __init__(self, config: SubagentConfig):
        self.config = config
        openai.api_key = settings.OPENAI_API_KEY
        self.name = config.name
        self.description = config.description
        self.capabilities = config.capabilities

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> SubagentResult:
        """
        Execute a task with the subagent
        """
        try:
            logger.info(f"Subagent {self.name} executing task: {task}")

            # Validate task against capabilities
            if not self._can_handle_task(task):
                return SubagentResult(
                    success=False,
                    message=f"Subagent {self.name} cannot handle task: {task}"
                )

            # Process the task
            result = await self._process_task(task, context)

            return result

        except Exception as e:
            logger.error(f"Error in subagent {self.name}: {str(e)}")
            return SubagentResult(
                success=False,
                message=f"Error in subagent {self.name}: {str(e)}"
            )

    def _can_handle_task(self, task: str) -> bool:
        """
        Check if this subagent can handle the given task
        """
        # Simple keyword matching for now - can be enhanced with semantic matching
        task_lower = task.lower()
        for capability in self.capabilities:
            if capability.lower() in task_lower:
                return True
        return False

    @abc.abstractmethod
    async def _process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> SubagentResult:
        """
        Process the specific task - to be implemented by subclasses
        """
        pass

    def _build_system_prompt(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build system prompt for the subagent
        """
        base_prompt = f"""
        You are {self.name}, a specialized AI assistant with the following capabilities: {', '.join(self.capabilities)}.
        Your role is to: {self.description}

        Task: {task}
        """

        if context:
            base_prompt += f"\nContext: {context}"

        base_prompt += "\nProvide a helpful, accurate response based on your specialized capabilities."

        return base_prompt