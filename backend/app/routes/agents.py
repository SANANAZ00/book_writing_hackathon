from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.agents.manager import agent_orchestrator

router = APIRouter()

class AgentRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = None
    agent_type: str = "auto"  # "subagent", "skill", or "auto"

class AgentResponse(BaseModel):
    success: bool
    result: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class SkillExecuteRequest(BaseModel):
    skill_name: str
    parameters: Dict[str, Any]

class SubagentExecuteRequest(BaseModel):
    subagent_name: str
    task: str
    context: Optional[Dict[str, Any]] = None

@router.post("/execute", response_model=AgentResponse)
async def execute_agent(request: AgentRequest):
    """
    Execute a task using the appropriate agent (subagent or skill)
    """
    try:
        result = await agent_orchestrator.execute_task(
            task=request.task,
            context=request.context,
            agent_type=request.agent_type
        )

        return AgentResponse(
            success=result.success,
            result=result.dict() if hasattr(result, 'dict') else {"data": result},
            message=result.message if hasattr(result, 'message') else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skill/execute", response_model=AgentResponse)
async def execute_skill(request: SkillExecuteRequest):
    """
    Execute a specific skill with parameters
    """
    try:
        result = await agent_orchestrator.skill_registry.execute_skill(
            request.skill_name,
            **request.parameters
        )

        return AgentResponse(
            success=result.success,
            result=result.dict() if hasattr(result, 'dict') else {"data": result},
            message=result.message if hasattr(result, 'message') else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/subagent/execute", response_model=AgentResponse)
async def execute_subagent(request: SubagentExecuteRequest):
    """
    Execute a specific subagent with task and context
    """
    try:
        result = await agent_orchestrator.subagent_manager.execute_subagent(
            request.subagent_name,
            request.task,
            request.context
        )

        return AgentResponse(
            success=result.success,
            result=result.dict() if hasattr(result, 'dict') else {"data": result},
            message=result.message if hasattr(result, 'message') else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available", response_model=Dict[str, Any])
async def get_available_agents():
    """
    Get information about all available agents (subagents and skills)
    """
    try:
        available = agent_orchestrator.get_available_agents()
        return available
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/subagents", response_model=Dict[str, Any])
async def list_subagents():
    """
    List all available subagents
    """
    try:
        subagents = agent_orchestrator.subagent_manager.list_subagents()
        details = {}
        for name in subagents:
            subagent = agent_orchestrator.subagent_manager.get_subagent(name)
            details[name] = {
                "description": subagent.description,
                "capabilities": subagent.capabilities
            }

        return {"subagents": details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skills", response_model=Dict[str, Any])
async def list_skills():
    """
    List all available skills
    """
    try:
        skills = agent_orchestrator.skill_registry.list_skills()
        details = {}
        for name in skills:
            skill = agent_orchestrator.skill_registry.get_skill(name)
            details[name] = {
                "description": skill.description,
                "parameters": skill.parameters,
                "required_params": skill.required_params
            }

        return {"skills": details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))