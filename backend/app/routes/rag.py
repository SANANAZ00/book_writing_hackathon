from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
import logging

from pydantic import BaseModel
from app.utils.rag import RAGPipeline, RetrievedDocument
from app.config import settings
from typing import Literal

logger = logging.getLogger(__name__)

router = APIRouter()

class RAGRequest(BaseModel):
    """Model for RAG request"""
    query: str
    provider: Optional[str] = settings.DEFAULT_PROVIDER
    model: Optional[str] = settings.DEFAULT_MODEL
    temperature: Optional[float] = settings.TEMPERATURE
    max_tokens: Optional[int] = settings.MAX_TOKENS
    search_limit: Optional[int] = settings.RAG_SEARCH_LIMIT
    score_threshold: Optional[float] = settings.RAG_SCORE_THRESHOLD


class RAGResponse(BaseModel):
    """Model for RAG response"""
    response: str
    sources: List[Dict[str, Any]]
    model_used: str
    provider: str
    usage: Optional[Dict[str, int]] = {}
    retrieved_documents: Optional[List[Dict[str, Any]]] = []


class SearchRequest(BaseModel):
    """Model for search-only request"""
    query: str
    limit: Optional[int] = settings.RAG_SEARCH_LIMIT
    score_threshold: Optional[float] = settings.RAG_SCORE_THRESHOLD


class SearchResponse(BaseModel):
    """Model for search response"""
    documents: List[Dict[str, Any]]
    total_found: int


@router.post("/", response_model=RAGResponse)
async def rag_query_endpoint(request: RAGRequest) -> RAGResponse:
    """
    RAG query endpoint that retrieves relevant documents and generates response
    """
    try:
        logger.info(f"Received RAG request - Provider: {request.provider}, Model: {request.model}")

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

        # Perform RAG query
        response = await rag_pipeline.query(
            query=request.query,
            provider=request.provider,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            search_limit=request.search_limit,
            score_threshold=request.score_threshold
        )

        logger.info(f"RAG query completed successfully using {response['provider']}/{response['model_used']}")

        return RAGResponse(**response)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in RAG endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing RAG request: {str(e)}"
        )


@router.post("/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest) -> SearchResponse:
    """
    Search endpoint that only retrieves relevant documents without generating response
    """
    try:
        logger.info(f"Received search request for: {request.query[:50]}...")

        # Initialize RAG pipeline to access search functionality
        rag_pipeline = RAGPipeline()

        # Perform search
        documents = await rag_pipeline.search_documents(
            query=request.query,
            limit=request.limit,
            score_threshold=request.score_threshold
        )

        # Convert to response format
        result_docs = []
        for doc in documents:
            result_docs.append({
                "id": doc.id,
                "content": doc.content,
                "score": doc.score,
                "metadata": doc.metadata
            })

        logger.info(f"Search completed successfully, found {len(result_docs)} documents")

        return SearchResponse(
            documents=result_docs,
            total_found=len(result_docs)
        )

    except Exception as e:
        logger.error(f"Unexpected error in search endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing search request: {str(e)}"
        )


class EmbedRequest(BaseModel):
    texts: List[str]
    input_type: Optional[Literal["search_document", "search_query", "classification", "clustering"]] = "search_document"


@router.post("/embed")
async def embed_text_endpoint(request: EmbedRequest):
    """
    Endpoint to generate embeddings for given texts
    """
    try:
        logger.info(f"Received embed request for {len(request.texts)} texts with input_type: {request.input_type}")

        from app.utils.llm_clients import LLMManager
        llm_manager = LLMManager()

        embeddings = await llm_manager.embed_texts(request.texts, input_type=request.input_type)

        logger.info(f"Generated embeddings for {len(request.texts)} texts")

        return {
            "embeddings": embeddings,
            "count": len(embeddings),
            "vector_dimension": len(embeddings[0]) if embeddings else 0,
            "input_type": request.input_type
        }

    except Exception as e:
        logger.error(f"Unexpected error in embed endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating embeddings: {str(e)}"
        )


@router.get("/collection-info")
async def get_collection_info():
    """
    Get information about the Qdrant collection
    """
    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=settings.QDRANT_GRPC_ENABLED,
            timeout=settings.QDRANT_TIMEOUT
        )

        collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)

        return {
            "name": collection_info.config.params.vectors.size,
            "vector_size": collection_info.config.params.vectors.size,
            "distance": collection_info.config.params.vectors.distance,
            "points_count": collection_info.points_count,
            "indexed_vectors_count": collection_info.indexed_vectors_count,
            "collection_exists": True
        }

    except Exception as e:
        logger.error(f"Error getting collection info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting collection info: {str(e)}"
        )


@router.post("/add-document")
async def add_document_endpoint(doc_id: str, content: str, metadata: Optional[Dict[str, Any]] = {}):
    """
    Add a document to the Qdrant collection
    """
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.http import models

        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=settings.QDRANT_GRPC_ENABLED,
            timeout=settings.QDRANT_TIMEOUT
        )

        from app.utils.llm_clients import LLMManager
        llm_manager = LLMManager()

        # Generate embedding for the content with correct input type
        embeddings = await llm_manager.embed_texts([content], input_type="search_document")
        vector = embeddings[0]

        # Create record
        records = [
            models.PointStruct(
                id=doc_id,
                vector=vector,
                payload={
                    "content": content,
                    "metadata": metadata
                }
            )
        ]

        # Upsert the record
        client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=records
        )

        logger.info(f"Added document to collection: {doc_id}")

        return {
            "success": True,
            "document_id": doc_id,
            "indexed": True
        }

    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error adding document: {str(e)}"
        )


@router.get("/health")
async def rag_health():
    """Health check for RAG service"""
    try:
        from app.utils.rag import RAGPipeline

        # Test RAG pipeline initialization
        rag_pipeline = RAGPipeline()

        # Test basic search functionality
        test_docs = await rag_pipeline.search_documents(query="test", limit=1)

        # Test basic generation functionality
        from app.utils.llm_clients import LLMManager
        llm_manager = LLMManager()
        test_messages = [{"role": "user", "content": "Hello"}]
        test_response = await llm_manager.generate_response(
            messages=test_messages,
            provider=settings.DEFAULT_PROVIDER,
            model=settings.DEFAULT_MODEL,
            max_tokens=10
        )

        return {
            "status": "healthy",
            "rag_pipeline_initialized": True,
            "search_functionality": True,
            "llm_functionality": True,
            "test_documents_found": len(test_docs) >= 0,  # Could be 0 if no docs in collection
            "test_generation_success": bool(test_response.get("response"))
        }
    except Exception as e:
        logger.error(f"RAG health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "rag_pipeline_initialized": False,
            "search_functionality": False,
            "llm_functionality": False
        }