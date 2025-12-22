#!/usr/bin/env python3
"""
Demonstration of API usage for the Physical AI book RAG chatbot
"""
import json

def show_api_usage():
    print("="*80)
    print("PHYSICAL AI BOOK RAG CHATBOT - API USAGE DEMO")
    print("="*80)

    print("\n1. MAIN BOOK CHAT ENDPOINT")
    print("-" * 40)
    print("POST /api/book-chat/")
    print()
    print("Request:")
    demo_request = {
        "message": "Explain the concept of Physical AI",
        "mode": "full_book",  # or "selected_text"
        "selected_text": "Optional text when using selected_text mode",
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 500,
        "session_id": "optional-session-id"
    }
    print(json.dumps(demo_request, indent=2))
    print()
    print("Response:")
    demo_response = {
        "response": "Physical AI is a field that combines robotics, machine learning, and control theory...",
        "sources": [
            {
                "id": "doc_123",
                "content": "Physical AI fundamentals explained in Chapter 1...",
                "score": 0.85,
                "metadata": {
                    "title": "Chapter 1: Fundamentals",
                    "section": "Introduction"
                }
            }
        ],
        "session_id": "session_456",
        "model_used": "gpt-4o-mini",
        "provider": "openai",
        "usage": {
            "prompt_tokens": 150,
            "completion_tokens": 85,
            "total_tokens": 235
        },
        "mode_used": "full_book"
    }
    print(json.dumps(demo_response, indent=2))

    print("\n2. SELECTED-TEXT MODE EXAMPLE")
    print("-" * 40)
    print("POST /api/book-chat/")
    print()
    print("Request for selected-text mode:")
    selected_text_request = {
        "message": "Explain this concept",
        "mode": "selected_text",
        "selected_text": "Physical AI is a field that combines robotics, machine learning, and control theory to create embodied intelligence. This approach emphasizes the importance of physical interaction with the environment for developing true artificial intelligence.",
        "provider": "openai",
        "model": "gpt-4o-mini"
    }
    print(json.dumps(selected_text_request, indent=2))

    print("\n3. MODE SWITCHING")
    print("-" * 40)
    print("POST /api/book-chat/mode-switch")
    print()
    switch_request = {
        "mode": "selected_text",  # or "full_book"
        "session_id": "session_456"
    }
    print(json.dumps(switch_request, indent=2))

    print("\n4. CONTENT CHECK")
    print("-" * 40)
    print("POST /api/book-chat/content-check")
    print()
    check_request = {
        "query": "embodied intelligence"
    }
    print(json.dumps(check_request, indent=2))

    check_response = {
        "content_exists": True,
        "relevant_sources": [
            {
                "id": "doc_789",
                "content": "Embodied intelligence is the theory that intelligence...",
                "score": 0.92,
                "metadata": {
                    "title": "Chapter 3: Embodied Cognition",
                    "section": "Physical Intelligence"
                }
            }
        ],
        "message": "Found 1 relevant section in the book"
    }
    print(json.dumps(check_response, indent=2))

    print("\n5. HEALTH CHECK")
    print("-" * 40)
    print("GET /api/book-chat/health")
    print()
    health_response = {
        "status": "healthy",
        "llm_connection": True,
        "rag_connection": True,
        "test_documents_found": True,
        "test_generation_success": True,
        "book_rag_service_available": True
    }
    print(json.dumps(health_response, indent=2))

    print("\n" + "="*80)
    print("KEY FEATURES DEMONSTRATED:")
    print("[FEATURE] Dual mode operation (full-book vs selected-text)")
    print("[FEATURE] Strict book content adherence")
    print("[FEATURE] Response grounding validation")
    print("[FEATURE] Source citation with chapter references")
    print("[FEATURE] Session management")
    print("[FEATURE] Error handling with graceful degradation")
    print("[FEATURE] Health monitoring")
    print("="*80)

if __name__ == "__main__":
    show_api_usage()