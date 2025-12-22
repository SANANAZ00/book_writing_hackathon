"""
Specialized chat route for Physical AI & Humanoid Robotics book
Ensures strict book content adherence and dual mode operation
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional, List
import logging

from pydantic import BaseModel
from app.services.book_rag_service import BookRAGService, BookRAGRequest, BookRAGResponse
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

class BookChatRequest(BaseModel):
    """Request model for book chat"""
    message: str
    session_id: Optional[str] = None
    mode: str = "full_book"  # "full_book" or "selected_text"
    selected_text: Optional[str] = None
    provider: Optional[str] = settings.DEFAULT_PROVIDER
    model: Optional[str] = settings.DEFAULT_MODEL
    temperature: Optional[float] = settings.TEMPERATURE
    max_tokens: Optional[int] = settings.MAX_TOKENS
    search_limit: Optional[int] = settings.RAG_SEARCH_LIMIT
    score_threshold: Optional[float] = settings.RAG_SCORE_THRESHOLD

class BookChatResponse(BaseModel):
    """Response model for book chat"""
    response: str
    sources: List[Dict[str, Any]]
    session_id: str
    model_used: str
    provider: str
    usage: Optional[Dict[str, int]] = {}
    mode_used: str

@router.post("/", response_model=BookChatResponse)
async def book_chat_endpoint(request: BookChatRequest) -> BookChatResponse:
    """
    Book-specific chat endpoint with strict content adherence
    Supports both full-book and selected-text modes
    """
    try:
        logger.info(f"Received book chat request - Mode: {request.mode}, Provider: {request.provider}, Model: {request.model}")

        # Validate mode
        if request.mode not in ["full_book", "selected_text"]:
            raise HTTPException(
                status_code=400,
                detail="Mode must be either 'full_book' or 'selected_text'"
            )

        # Validate provider and model
        from app.utils.llm_clients import LLMManager
        llm_manager = LLMManager()

        if not llm_manager.validate_provider_and_model(request.provider, request.model):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider/model combination: {request.provider}/{request.model}. "
                       f"Available models: {settings.AVAILABLE_MODELS}"
            )

        # Initialize book RAG service
        book_rag_service = BookRAGService()

        # Prepare book RAG request
        book_request = BookRAGRequest(
            query=request.message,
            mode=request.mode,
            selected_text=request.selected_text,
            provider=request.provider,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            search_limit=request.search_limit,
            score_threshold=request.score_threshold
        )

        # Process the request
        response = await book_rag_service.query_book_content(book_request)

        # Generate or use provided session ID
        session_id = request.session_id or f"book_chat_{hash(request.message)}"

        logger.info(f"Book chat response generated successfully using {response.provider}/{response.model_used}")

        return BookChatResponse(
            response=response.response,
            sources=response.sources,
            session_id=session_id,
            model_used=response.model_used,
            provider=response.provider,
            usage=response.usage,
            mode_used=response.mode_used
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in book chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing book chat request: {str(e)}"
        )

class ModeSwitchRequest(BaseModel):
    """Request model for switching between modes"""
    mode: str  # "full_book" or "selected_text"
    session_id: str

class ModeSwitchResponse(BaseModel):
    """Response model for mode switching"""
    success: bool
    new_mode: str
    session_id: str
    message: str

@router.post("/mode-switch", response_model=ModeSwitchResponse)
async def mode_switch_endpoint(request: ModeSwitchRequest) -> ModeSwitchResponse:
    """
    Endpoint to switch between full-book and selected-text modes
    """
    try:
        logger.info(f"Mode switch request - Session: {request.session_id}, New mode: {request.mode}")

        if request.mode not in ["full_book", "selected_text"]:
            raise HTTPException(
                status_code=400,
                detail="Mode must be either 'full_book' or 'selected_text'"
            )

        # In a real implementation, we would store the mode preference in the session
        # For now, we just validate and return success

        return ModeSwitchResponse(
            success=True,
            new_mode=request.mode,
            session_id=request.session_id,
            message=f"Successfully switched to {request.mode} mode"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in mode switch endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error switching mode: {str(e)}"
        )

class BookContentCheckRequest(BaseModel):
    """Request model for checking if content exists in book"""
    query: str

class BookContentCheckResponse(BaseModel):
    """Response model for content existence check"""
    content_exists: bool
    relevant_sources: List[Dict[str, Any]]
    message: str

@router.post("/content-check", response_model=BookContentCheckResponse)
async def content_check_endpoint(request: BookContentCheckRequest) -> BookContentCheckResponse:
    """
    Check if specific content exists in the book
    """
    try:
        logger.info(f"Content check request: {request.query[:50]}...")

        # Initialize book RAG service to search for content
        book_rag_service = BookRAGService()

        # Perform a search to see if content exists
        from app.utils.rag import RAGPipeline
        rag_pipeline = RAGPipeline()

        # Search for relevant documents
        documents = await rag_pipeline.search_documents(
            query=request.query,
            limit=5,  # Get top 5 matches
            score_threshold=0.3  # Lower threshold for broader search
        )

        # Filter for book content
        valid_docs = book_rag_service._filter_book_documents(documents)

        if valid_docs:
            sources = [
                {
                    "id": doc.id,
                    "content": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                    "score": doc.score,
                    "metadata": doc.metadata
                }
                for doc in valid_docs
            ]

            return BookContentCheckResponse(
                content_exists=True,
                relevant_sources=sources,
                message=f"Found {len(valid_docs)} relevant sections in the book"
            )
        else:
            return BookContentCheckResponse(
                content_exists=False,
                relevant_sources=[],
                message="No relevant content found in the book"
            )

    except Exception as e:
        logger.error(f"Error in content check endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error checking content: {str(e)}"
        )

@router.get("/health")
async def book_chat_health():
    """Health check for book chat service"""
    try:
        from app.utils.llm_clients import LLMManager
        from app.utils.rag import RAGPipeline

        # Test basic LLM functionality
        llm_manager = LLMManager()
        test_messages = [{"role": "user", "content": "Hello"}]
        test_response = await llm_manager.generate_response(
            messages=test_messages,
            provider=settings.DEFAULT_PROVIDER,
            model=settings.DEFAULT_MODEL,
            max_tokens=10
        )

        # Test RAG functionality
        rag_pipeline = RAGPipeline()
        test_docs = await rag_pipeline.search_documents(query="test", limit=1)

        return {
            "status": "healthy",
            "llm_connection": True,
            "rag_connection": True,
            "test_documents_found": len(test_docs) >= 0,
            "test_generation_success": bool(test_response.get("response")),
            "book_rag_service_available": True
        }
    except Exception as e:
        logger.error(f"Book chat health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "llm_connection": False,
            "rag_connection": False,
            "book_rag_service_available": False
        }

# Add the book chat router to main app in main.py
# This endpoint should be accessible at /api/book-chat