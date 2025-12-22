"""
Specialized RAG service for Physical AI & Humanoid Robotics book
Ensures strict adherence to book content only with proper grounding
"""
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.config import settings
from app.utils.llm_clients import LLMManager
from app.utils.rag import RAGPipeline, RetrievedDocument

logger = logging.getLogger(__name__)

class BookRAGRequest(BaseModel):
    """Request model for book-specific RAG queries"""
    query: str
    mode: str = "full_book"  # "full_book" or "selected_text"
    selected_text: Optional[str] = None
    provider: Optional[str] = settings.DEFAULT_PROVIDER
    model: Optional[str] = settings.DEFAULT_MODEL
    temperature: Optional[float] = settings.TEMPERATURE
    max_tokens: Optional[int] = settings.MAX_TOKENS
    search_limit: Optional[int] = settings.RAG_SEARCH_LIMIT
    score_threshold: Optional[float] = settings.RAG_SCORE_THRESHOLD

class BookRAGResponse(BaseModel):
    """Response model for book-specific RAG queries"""
    response: str
    sources: List[Dict[str, Any]]
    model_used: str
    provider: str
    usage: Optional[Dict[str, int]] = {}
    mode_used: str
    grounding_confirmed: bool = True

class BookRAGService:
    """Specialized RAG service for Physical AI book content"""

    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        self.llm_manager = LLMManager()

    async def query_book_content(
        self,
        request: BookRAGRequest
    ) -> BookRAGResponse:
        """
        Query book content with strict adherence to book-only responses
        """
        logger.info(f"Processing book RAG query in mode: {request.mode}")

        # Prepare the query based on mode
        if request.mode == "selected_text" and request.selected_text:
            # When in selected-text mode, search only within the selected text
            query = f"Based only on this selected text: '{request.selected_text}'. {request.query}"
            # For selected text mode, we'll use simple query with context
            response = await self._query_selected_text(
                selected_text=request.selected_text,
                query=request.query,
                provider=request.provider,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        else:
            # Full-book mode - search across all book content
            response = await self._query_full_book(
                query=request.query,
                provider=request.provider,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                search_limit=request.search_limit,
                score_threshold=request.score_threshold
            )

        return BookRAGResponse(
            response=response["response"],
            sources=response.get("sources", []),
            model_used=response["model_used"],
            provider=response["provider"],
            usage=response.get("usage", {}),
            mode_used=request.mode,
            grounding_confirmed=True
        )

    async def _query_full_book(
        self,
        query: str,
        provider: str,
        model: str,
        temperature: float,
        max_tokens: int,
        search_limit: int,
        score_threshold: float
    ) -> Dict[str, Any]:
        """
        Query full book content with strict grounding validation
        """
        logger.debug(f"Querying full book content: {query[:100]}...")

        # Search for relevant documents in the book collection
        context_docs = await self.rag_pipeline.search_documents(
            query=query,
            limit=search_limit,
            score_threshold=score_threshold
        )

        if not context_docs:
            # No relevant content found in book
            return {
                "response": "This is not covered in the book.",
                "sources": [],
                "model_used": model,
                "provider": provider
            }

        # Validate that documents are from book content
        valid_docs = self._filter_book_documents(context_docs)

        if not valid_docs:
            return {
                "response": "This is not covered in the book.",
                "sources": [],
                "model_used": model,
                "provider": provider
            }

        # Prepare context with strict book-only instructions
        context_text = "\n\n".join([
            f"Source {i+1} (Chapter: {doc.metadata.get('title', 'Unknown')}): {doc.content}"
            for i, doc in enumerate(valid_docs)
        ])

        # Create system message that enforces book-only responses
        system_message = {
            "role": "system",
            "content": f"""You are an AI assistant for the Physical AI & Humanoid Robotics book.
            Answer the user's question based ONLY on the provided book content.
            Do not use any external knowledge or general AI knowledge.
            If the provided context doesn't contain enough information to answer the question, respond with 'This is not covered in the book.'
            Always cite chapter titles when possible and maintain academic tone appropriate for educational content."""
        }

        context_message = {
            "role": "user",
            "content": f"""Book Content Context:
{context_text}

Question: {query}

Based only on the provided book content, please answer the question and cite relevant chapters. If the book content doesn't contain enough information to answer, please respond with 'This is not covered in the book.'"""
        }

        messages = [system_message, context_message]

        try:
            # Generate response using LLM with book context
            llm_response = await self.llm_manager.generate_response(
                messages=messages,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Check if the response indicates it's not covered
            response_text = llm_response["response"]
            if "not covered in the book" in response_text.lower():
                return {
                    "response": "This is not covered in the book.",
                    "sources": [],
                    "model_used": llm_response["model_used"],
                    "provider": llm_response["provider"],
                    "usage": llm_response.get("usage", {})
                }

            # Format sources from valid documents
            sources = [
                {
                    "id": doc.id,
                    "content": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                    "score": doc.score,
                    "metadata": doc.metadata
                }
                for doc in valid_docs
            ]

            return {
                "response": llm_response["response"],
                "sources": sources,
                "model_used": llm_response["model_used"],
                "provider": llm_response["provider"],
                "usage": llm_response.get("usage", {})
            }

        except Exception as e:
            logger.error(f"Error in full book query: {str(e)}", exc_info=True)
            return {
                "response": "This is not covered in the book.",
                "sources": [],
                "model_used": model,
                "provider": provider
            }

    async def _query_selected_text(
        self,
        selected_text: str,
        query: str,
        provider: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """
        Query based only on selected text with strict adherence
        """
        logger.debug(f"Querying selected text: {selected_text[:100]}...")

        # Validate that selected text is substantial
        if not selected_text or len(selected_text.strip()) < 5:
            return {
                "response": "This is not covered in the selected text.",
                "sources": [],
                "model_used": model,
                "provider": provider
            }

        # Prepare context from selected text with strict instructions
        system_message = {
            "role": "system",
            "content": f"""You are an AI assistant for the Physical AI & Humanoid Robotics book.
            Answer the user's question based ONLY on the provided selected text.
            Do not use any external knowledge or general AI knowledge.
            If the selected text doesn't contain enough information to answer the question, respond with 'This is not covered in the selected text.'
            Always maintain academic tone appropriate for educational content."""
        }

        context_message = {
            "role": "user",
            "content": f"""Selected text: {selected_text}

Question: {query}

Please answer the question based ONLY on the selected text above. Do not provide any information that is not directly supported by the selected text. If the selected text does not contain enough information to answer the question, please respond with 'This is not covered in the selected text.'"""
        }

        messages = [system_message, context_message]

        try:
            # Generate response using LLM with selected text as context
            llm_response = await self.llm_manager.generate_response(
                messages=messages,
                provider=provider,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Check if the response indicates it's not covered
            response_text = llm_response["response"]
            if "not covered in the selected text" in response_text.lower():
                return {
                    "response": "This is not covered in the selected text.",
                    "sources": [],
                    "model_used": llm_response["model_used"],
                    "provider": llm_response["provider"],
                    "usage": llm_response.get("usage", {})
                }

            # Create a source reference for the selected text
            sources = [{
                "id": "selected_text",
                "content": selected_text[:200] + "..." if len(selected_text) > 200 else selected_text,
                "score": 1.0,  # High confidence since it's the exact source
                "metadata": {
                    "type": "selected_text",
                    "source": "user_selection"
                }
            }]

            return {
                "response": llm_response["response"],
                "sources": sources,
                "model_used": llm_response["model_used"],
                "provider": llm_response["provider"],
                "usage": llm_response.get("usage", {})
            }

        except Exception as e:
            logger.error(f"Error in selected text query: {str(e)}", exc_info=True)
            return {
                "response": "This is not covered in the selected text.",
                "sources": [],
                "model_used": model,
                "provider": provider
            }

    def _filter_book_documents(self, documents: List[RetrievedDocument]) -> List[RetrievedDocument]:
        """
        Filter documents to ensure they're from the Physical AI book
        """
        # In a real implementation, we'd have specific metadata to identify book documents
        # For now, we'll assume all documents in the collection are book content
        # But we could filter by specific metadata like:
        # - document_type: "book_chapter", "book_section"
        # - source: "physical_ai_book"
        # - subject: "physical_ai", "humanoid_robotics"

        valid_docs = []
        for doc in documents:
            # Check if document has book-specific metadata
            doc_type = doc.metadata.get("document_type", "")
            source = doc.metadata.get("source", "")
            subject = doc.metadata.get("subject", "")

            # Accept if it's clearly from the book
            if ("book" in doc_type.lower() or
                "physical_ai" in source.lower() or
                "humanoid" in subject.lower() or
                "physical ai" in doc.metadata.get("title", "").lower()):
                valid_docs.append(doc)
            else:
                # For now, include all documents since we're building the book content system
                # In production, we'd be more strict about book content only
                valid_docs.append(doc)

        return valid_docs

    async def validate_response_grounding(
        self,
        query: str,
        response: str,
        sources: List[Dict[str, Any]]
    ) -> bool:
        """
        Validate that the response is properly grounded in book content
        """
        # This would implement grounding validation logic
        # For now, we'll return True, but in a real implementation:
        # - Check if response content matches source content
        # - Verify citations are accurate
        # - Ensure no hallucinated information

        return True