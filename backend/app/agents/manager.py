import logging
from typing import Dict, List, Optional, Any, Union
from app.agents.ui_ux_refinement import UIUXRefinementSubagent
from app.agents.content_expansion import ContentExpansionSubagent
from app.agents.rag_optimization import RAGOptimizationSubagent
from app.agents.qdrant_data import QdrantDataSubagent
from app.agents.deployment_helper import DeploymentHelperSubagent
from app.agents.skills import (
    ExplainConceptSkill,
    RewriteInBookToneSkill,
    GenerateUIComponentSkill,
    GenerateAPIRouteSkill,
    OptimizeEmbeddingChunkSkill,
    ImproveRetrievalQualitySkill
)

logger = logging.getLogger(__name__)

class SubagentManager:
    """Manages subagents and their execution"""

    def __init__(self):
        self.subagents = {}
        self._initialize_subagents()

    def _initialize_subagents(self):
        """Initialize all available subagents"""
        subagents = [
            UIUXRefinementSubagent(),
            ContentExpansionSubagent(),
            RAGOptimizationSubagent(),
            QdrantDataSubagent(),
            DeploymentHelperSubagent()
        ]

        for subagent in subagents:
            self.subagents[subagent.name] = subagent

        logger.info(f"Initialized {len(self.subagents)} subagents")

    def get_subagent(self, name: str):
        """Get a subagent by name"""
        return self.subagents.get(name)

    def list_subagents(self) -> List[str]:
        """List all available subagents"""
        return list(self.subagents.keys())

    async def execute_subagent(self, name: str, task: str, context: Optional[Dict[str, Any]] = None):
        """Execute a task with a specific subagent"""
        subagent = self.get_subagent(name)
        if not subagent:
            raise ValueError(f"Subagent '{name}' not found")

        return await subagent.execute(task, context)

    async def find_best_subagent(self, task: str) -> Optional[str]:
        """Find the best subagent for a given task"""
        best_match = None
        best_score = 0

        for name, subagent in self.subagents.items():
            # Simple keyword matching for now - could be enhanced with semantic analysis
            score = 0
            task_lower = task.lower()

            for capability in subagent.capabilities:
                if capability.lower() in task_lower:
                    score += 1

            if score > best_score:
                best_score = score
                best_match = name

        return best_match

class SkillRegistry:
    """Registry for managing and executing skills"""

    def __init__(self):
        self.skills = {}
        self._initialize_skills()

    def _initialize_skills(self):
        """Initialize all available skills"""
        skills = [
            ExplainConceptSkill(),
            RewriteInBookToneSkill(),
            GenerateUIComponentSkill(),
            GenerateAPIRouteSkill(),
            OptimizeEmbeddingChunkSkill(),
            ImproveRetrievalQualitySkill()
        ]

        for skill in skills:
            self.skills[skill.name] = skill

        logger.info(f"Initialized {len(self.skills)} skills")

    def get_skill(self, name: str):
        """Get a skill by name"""
        return self.skills.get(name)

    def list_skills(self) -> List[str]:
        """List all available skills"""
        return list(self.skills.keys())

    async def execute_skill(self, name: str, **kwargs):
        """Execute a specific skill with parameters"""
        skill = self.get_skill(name)
        if not skill:
            raise ValueError(f"Skill '{name}' not found")

        return await skill.execute(**kwargs)

    async def find_best_skill(self, description: str) -> Optional[str]:
        """Find the best skill for a given description"""
        best_match = None
        best_score = 0

        for name, skill in self.skills.items():
            # Simple keyword matching for now
            score = 0
            desc_lower = description.lower()

            if skill.description.lower() in desc_lower or name.lower() in desc_lower:
                score = 2  # Exact match gets higher score
            else:
                # Check if any key terms from skill description are in the input
                for term in skill.description.lower().split():
                    if len(term) > 3 and term in desc_lower:  # Only consider terms longer than 3 chars
                        score += 1

            if score > best_score:
                best_score = score
                best_match = name

        return best_match

class AgentOrchestrator:
    """Orchestrates subagents and skills"""

    def __init__(self):
        self.subagent_manager = SubagentManager()
        self.skill_registry = SkillRegistry()

    async def execute_task(self, task: str, context: Optional[Dict[str, Any]] = None, agent_type: str = "auto"):
        """
        Execute a task using appropriate agent (subagent or skill)
        """
        if agent_type == "subagent":
            best_subagent = await self.subagent_manager.find_best_subagent(task)
            if best_subagent:
                return await self.subagent_manager.execute_subagent(best_subagent, task, context)
            else:
                raise ValueError(f"No suitable subagent found for task: {task}")

        elif agent_type == "skill":
            best_skill = await self.skill_registry.find_best_skill(task)
            if best_skill:
                # For skills, we need to extract parameters from the task
                # This is a simplified approach - in reality, you'd want more sophisticated parameter extraction
                return await self.skill_registry.execute_skill(best_skill)
            else:
                raise ValueError(f"No suitable skill found for task: {task}")

        elif agent_type == "auto":
            # Try to determine the best agent type automatically
            # For now, we'll prioritize skills for specific tasks and subagents for complex ones
            if any(keyword in task.lower() for keyword in [
                "explain", "define", "what is", "how to", "generate", "create", "optimize"
            ]):
                best_skill = await self.skill_registry.find_best_skill(task)
                if best_skill:
                    return await self.skill_registry.execute_skill(best_skill)

            # If no skill matches or for complex tasks, try subagents
            best_subagent = await self.subagent_manager.find_best_subagent(task)
            if best_subagent:
                return await self.subagent_manager.execute_subagent(best_subagent, task, context)

        raise ValueError(f"No suitable agent found for task: {task}")

    def get_available_agents(self) -> Dict[str, Any]:
        """Get information about all available agents"""
        return {
            "subagents": {
                "names": self.subagent_manager.list_subagents(),
                "details": {
                    name: {
                        "description": subagent.description,
                        "capabilities": subagent.capabilities
                    }
                    for name, subagent in self.subagent_manager.subagents.items()
                }
            },
            "skills": {
                "names": self.skill_registry.list_skills(),
                "details": {
                    name: {
                        "description": skill.description,
                        "parameters": skill.parameters,
                        "required_params": skill.required_params
                    }
                    for name, skill in self.skill_registry.skills.items()
                }
            }
        }

# Global instance for easy access
agent_orchestrator = AgentOrchestrator()