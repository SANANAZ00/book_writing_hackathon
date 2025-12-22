from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, Optional, List
import logging

from pydantic import BaseModel
from app.utils.rag import RAGPipeline
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessage(BaseModel):
    """Model for individual chat messages"""
    role: str  # "user", "assistant", "system"
    content: str


class ChatRequest(BaseModel):
    """Model for chat request"""
    message: str
    history: Optional[List[ChatMessage]] = []
    provider: Optional[str] = settings.DEFAULT_PROVIDER
    model: Optional[str] = settings.DEFAULT_MODEL
    temperature: Optional[float] = settings.TEMPERATURE
    max_tokens: Optional[int] = settings.MAX_TOKENS
    use_rag: Optional[bool] = True  # Whether to use RAG context
    search_limit: Optional[int] = settings.RAG_SEARCH_LIMIT
    score_threshold: Optional[float] = settings.RAG_SCORE_THRESHOLD
    selected_text: Optional[str] = None  # Selected text for context


class ChatResponse(BaseModel):
    """Model for chat response"""
    response: str
    sources: List[Dict[str, Any]]
    model_used: str
    provider: str
    usage: Optional[Dict[str, int]] = {}
    error: Optional[str] = None


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint supporting both OpenAI and Cohere with RAG capabilities
    Defaults to Cohere command-r if no model is specified
    """
    try:
        logger.info(f"Received chat request - Provider: {request.provider}, Model: {request.model}, Use RAG: {request.use_rag}")

        # Validate provider and model
        from app.utils.llm_clients import LLMManager
        llm_manager = LLMManager()

        if not llm_manager.validate_provider_and_model(request.provider, request.model):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider/model combination: {request.provider}/{request.model}. "
                       f"Available models: {settings.AVAILABLE_MODELS}"
            )

        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline()

        # Prepare query - include selected text in context if provided
        query = request.message
        if request.selected_text:
            query = f"Considering this selected text: '{request.selected_text}'. {request.message}"

        # Use RAG if enabled and collection has documents, otherwise fallback to simple query
        if request.use_rag:
            # First check if collection has any documents
            try:
                from qdrant_client import QdrantClient
                qdrant_client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                    prefer_grpc=settings.QDRANT_GRPC_ENABLED,
                    timeout=settings.QDRANT_TIMEOUT
                )
                collection_info = qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)
                logger.info(f"Qdrant collection '{settings.QDRANT_COLLECTION_NAME}' has {collection_info.points_count} documents")

                if collection_info.points_count > 0:
                    # Collection has documents, use RAG
                    logger.info(f"Using RAG with search_limit: {request.search_limit}, score_threshold: {request.score_threshold}")
                    response = await rag_pipeline.query(
                        query=query,
                        provider=request.provider,
                        model=request.model,
                        temperature=request.temperature,
                        max_tokens=request.max_tokens,
                        search_limit=request.search_limit,
                        score_threshold=request.score_threshold
                    )
                    logger.info(f"RAG query completed with {len(response.get('sources', []))} sources")
                else:
                    # No documents in collection, fallback to simple query
                    logger.warning("Qdrant collection is empty, falling back to simple query")
                    response = await rag_pipeline.simple_query(
                        query=query,
                        provider=request.provider,
                        model=request.model,
                        temperature=request.temperature,
                        max_tokens=request.max_tokens
                    )
                    response["sources"] = []  # No sources available in simple query
                    response["warning"] = "Knowledge base is empty, using model knowledge only"
            except Exception as e:
                logger.error(f"Error checking Qdrant collection: {str(e)}, falling back to simple query")
                # Fallback to simple query if Qdrant is unavailable
                response = await rag_pipeline.simple_query(
                    query=query,
                    provider=request.provider,
                    model=request.model,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                )
                response["sources"] = []
                response["warning"] = "Knowledge base temporarily unavailable, using model knowledge only"
        else:
            # Always use simple query when use_rag=False
            response = await rag_pipeline.simple_query(
                query=query,
                provider=request.provider,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )

        logger.info(f"Chat response generated successfully using {response['provider']}/{response['model_used']}")

        return ChatResponse(**response)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        return ChatResponse(
            response="Sorry, I encountered an error. Please try again.",
            sources=[],
            model_used=request.model,
            provider=request.provider,
            error=str(e)
        )


@router.get("/models")
async def get_available_models() -> Dict[str, Any]:
    """Get list of available models for both providers"""
    return {
        "default_provider": settings.DEFAULT_PROVIDER,
        "default_model": settings.DEFAULT_MODEL,
        "available_models": settings.AVAILABLE_MODELS,
        "providers": list(settings.AVAILABLE_MODELS.keys())
    }


@router.post("/debug")
async def debug_chat(request: ChatRequest):
    """Debug endpoint to test chat functionality without RAG"""
    try:
        from app.utils.rag import RAGPipeline
        rag_pipeline = RAGPipeline()

        # Simple query without RAG for debugging
        response = await rag_pipeline.simple_query(
            query=request.message,
            provider=request.provider,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return response
    except Exception as e:
        logger.error(f"Debug chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def chat_health():
    """Health check for chat service using Cohere as default"""
    try:
        from app.utils.llm_clients import LLMManager
        llm_manager = LLMManager()

        # Test basic LLM functionality
        test_messages = [{"role": "user", "content": "Hello"}]
        test_response = await llm_manager.generate_response(
            messages=test_messages,
            provider=settings.DEFAULT_PROVIDER,
            model=settings.DEFAULT_MODEL,
            max_tokens=10
        )

        # Check Qdrant connection
        from qdrant_client import QdrantClient
        qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=settings.QDRANT_GRPC_ENABLED,
            timeout=settings.QDRANT_TIMEOUT
        )

        # Get collection info to verify connectivity
        collection_info = qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)

        return {
            "status": "healthy",
            "llm_connection": True,
            "qdrant_connection": True,
            "collection_exists": True,
            "collection_points": collection_info.points_count,
            "test_generation_success": bool(test_response.get("response"))
        }
    except Exception as e:
        logger.error(f"Chat health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "llm_connection": False,
            "qdrant_connection": False
        }