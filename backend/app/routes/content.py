from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
import logging

from pydantic import BaseModel
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

class ContentRequest(BaseModel):
    """Model for content-related requests"""
    content: str
    section_title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class ContentResponse(BaseModel):
    """Model for content-related responses"""
    success: bool
    message: str
    content_id: Optional[str] = None


@router.get("/")
async def content_root():
    return {"message": "Content API endpoint", "version": "1.0.0"}


@router.get("/health")
async def content_health():
    """Health check for content service"""
    return {
        "status": "healthy",
        "message": "Content service is operational"
    }


@router.get("/info")
async def get_content_info():
    """Get information about the content service"""
    return {
        "service": "Content Management",
        "version": "1.0.0",
        "features": [
            "Document indexing",
            "Content search",
            "RAG integration",
            "Multi-LLM support"
        ],
        "default_provider": settings.DEFAULT_PROVIDER,
        "default_model": settings.DEFAULT_MODEL
    }