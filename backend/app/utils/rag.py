"""
Utility module for RAG (Retrieval Augmented Generation) functionality
"""
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.config import settings
from app.utils.llm_clients import LLMManager

logger = logging.getLogger(__name__)

class RetrievedDocument(BaseModel):
    """Model representing a retrieved document from vector store"""
    id: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}


class RAGPipeline:
    """Main RAG pipeline class"""
    
    def __init__(self):
        self.llm_manager = LLMManager()
        self.client = None
        self._initialize_qdrant_client()
    
    def _initialize_qdrant_client(self):
        """Initialize Qdrant client"""
        try:
            logger.info(f"Initializing Qdrant client for collection: {settings.QDRANT_COLLECTION_NAME}")
            from qdrant_client import QdrantClient
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                prefer_grpc=settings.QDRANT_GRPC_ENABLED,
                timeout=settings.QDRANT_TIMEOUT
            )
            logger.info("Qdrant client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {str(e)}", exc_info=True)
            raise

    async def search_documents(
        self,
        query: str,
        limit: int = settings.RAG_SEARCH_LIMIT,
        score_threshold: float = settings.RAG_SCORE_THRESHOLD
    ) -> List[RetrievedDocument]:
        """
        Search for relevant documents in Qdrant

        Args:
            query: Query string to search for
            limit: Number of documents to retrieve
            score_threshold: Minimum similarity score threshold

        Returns:
            List of retrieved documents with scores
        """
        try:
            logger.debug(f"Starting document search for query: {query[:100]}...")
            logger.debug(f"Search parameters - limit: {limit}, score_threshold: {score_threshold}")

            # Generate embedding for the query with correct input type
            embeddings = await self.llm_manager.embed_texts([query], input_type="search_query")
            query_vector = embeddings[0]
            logger.debug(f"Generated embedding vector of size: {len(query_vector)}")
            logger.debug(f"Query embedding (first 5 values): {query_vector[:5]}")

            # Search in Qdrant using query_points
            logger.debug(f"Qdrant search called with collection: {settings.QDRANT_COLLECTION_NAME}, limit: {limit}, score_threshold: {score_threshold}")
            response = self.client.query_points(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                query=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True
            )

            # Extract points from the response
            results = response.points
            logger.info(f"Qdrant returned {len(results)} raw results")
            logger.debug(f"Raw result scores: {[result.score for result in results]}")

            # Convert results to RetrievedDocument objects
            documents = []
            for result in results:
                doc = RetrievedDocument(
                    id=str(result.id),
                    content=result.payload.get("content", ""),
                    score=result.score,
                    metadata=result.payload.get("metadata", {})
                )
                documents.append(doc)

            logger.info(f"Found {len(documents)} documents for query: {query[:50]}...")
            logger.debug(f"Document scores: {[doc.score for doc in documents]}")

            # Log why sources might be empty
            if len(documents) == 0:
                logger.warning(f"No documents returned from Qdrant search. Query: '{query[:100]}...', score_threshold: {score_threshold}, limit: {limit}")
                # Check if collection exists and has documents
                try:
                    collection_info = self.client.get_collection(settings.QDRANT_COLLECTION_NAME)
                    logger.info(f"Collection '{settings.QDRANT_COLLECTION_NAME}' has {collection_info.points_count} points")
                except Exception as e:
                    logger.error(f"Error getting collection info: {str(e)}")

            return documents

        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}", exc_info=True)
            # Return empty list instead of raising to maintain graceful degradation
            return []

    async def generate_with_context(
        self,
        query: str,
        context_docs: List[RetrievedDocument],
        provider: str = settings.DEFAULT_PROVIDER,
        model: str = settings.DEFAULT_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS
    ) -> Dict[str, Any]:
        """
        Generate response using LLM with retrieved context

        Args:
            query: Original user query
            context_docs: Retrieved context documents
            provider: LLM provider to use
            model: LLM model to use
            temperature: Generation temperature
            max_tokens: Max tokens to generate

        Returns:
            Dictionary with response, sources, and model info
        """
        try:
            logger.debug(f"Starting RAG generation with {len(context_docs)} context documents")
            logger.debug(f"Query length: {len(query)}, Provider: {provider}, Model: {model}")

            # Prepare context from retrieved documents
            context_text = "\n\n".join([
                f"Source {i+1}: {doc.content}"
                for i, doc in enumerate(context_docs)
            ])

            logger.debug(f"Context text length: {len(context_text)}")

            # Prepare system and user messages
            system_message = {
                "role": "system",
                "content": f"""You are a helpful AI assistant that answers questions based on provided documentation.
                Use only the context provided below to answer the user's question.
                If the context doesn't contain enough information, say so.
                Always cite sources when possible."""
            }

            context_message = {
                "role": "user",
                "content": f"""Context: {context_text}\n\nQuestion: {query}\n\nBased on the provided context, please answer the question and cite relevant sources. If the context doesn't contain enough information to answer, please say so."""
            }

            messages = [system_message, context_message]

            # Generate response using LLM
            llm_response = await self.llm_manager.generate_response(
                messages=messages,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Add sources to response
            sources = [
                {
                    "id": doc.id,
                    "content": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,  # Truncate for response
                    "score": doc.score,
                    "metadata": doc.metadata
                }
                for doc in context_docs
            ]

            # Combine LLM response with RAG information
            result = {
                "response": llm_response["response"],
                "sources": sources,
                "model_used": llm_response["model_used"],
                "provider": llm_response["provider"],
                "usage": llm_response.get("usage", {})
            }

            logger.info(f"Generated RAG response using {provider}/{model} with {len(sources)} sources")
            return result

        except Exception as e:
            logger.error(f"Error in RAG generation: {str(e)}", exc_info=True)
            raise

    async def query(
        self,
        query: str,
        provider: str = settings.DEFAULT_PROVIDER,
        model: str = settings.DEFAULT_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS,
        search_limit: int = settings.RAG_SEARCH_LIMIT,
        score_threshold: float = settings.RAG_SCORE_THRESHOLD
    ) -> Dict[str, Any]:
        """
        Main RAG query method that combines search and generation

        Args:
            query: User query
            provider: LLM provider to use
            model: LLM model to use
            temperature: Generation temperature
            max_tokens: Max tokens to generate
            search_limit: Number of documents to retrieve
            score_threshold: Minimum similarity score threshold

        Returns:
            Dictionary with complete RAG response
        """
        try:
            logger.info(f"Starting RAG query with {provider}/{model} for: {query[:50]}...")
            logger.debug(f"RAG parameters - search_limit: {search_limit}, score_threshold: {score_threshold}, max_tokens: {max_tokens}")

            # Search for relevant documents
            context_docs = await self.search_documents(
                query=query,
                limit=search_limit,
                score_threshold=score_threshold
            )

            logger.debug(f"Retrieved {len(context_docs)} context documents for RAG")

            # Generate response with context
            response = await self.generate_with_context(
                query=query,
                context_docs=context_docs,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )

            logger.info(f"RAG query completed successfully with {len(response['sources'])} sources")
            return response

        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}", exc_info=True)
            # Return error response instead of raising to maintain API consistency
            return {
                "error": "An error occurred while processing your request",
                "response": "Sorry, I encountered an error. Please try again.",
                "sources": [],
                "model_used": model,
                "provider": provider
            }

    async def simple_query(
        self,
        query: str,
        provider: str = settings.DEFAULT_PROVIDER,
        model: str = settings.DEFAULT_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS
    ) -> Dict[str, Any]:
        """
        Simple query without RAG context (for comparison)
        """
        try:
            logger.debug(f"Starting simple query with {provider}/{model} for: {query[:50]}...")

            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]

            llm_response = await self.llm_manager.generate_response(
                messages=messages,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )

            result = {
                "response": llm_response["response"],
                "sources": [],
                "model_used": llm_response["model_used"],
                "provider": llm_response["provider"],
                "usage": llm_response.get("usage", {})
            }

            logger.info(f"Simple query completed successfully using {provider}/{model}")
            return result

        except Exception as e:
            logger.error(f"Error in simple query: {str(e)}", exc_info=True)
            return {
                "error": "An error occurred while processing your request",
                "response": "Sorry, I encountered an error. Please try again.",
                "sources": [],
                "model_used": model,
                "provider": provider
            }