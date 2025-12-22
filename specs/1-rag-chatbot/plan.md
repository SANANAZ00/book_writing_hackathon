# Implementation Plan: RAG Chatbot for Physical AI & Humanoid Robotics Book

**Branch**: `1-rag-chatbot` | **Date**: 2025-12-20 | **Spec**: [specs/1-rag-chatbot/spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a RAG (Retrieval-Augmented Generation) chatbot for the Physical AI & Humanoid Robotics book that allows users to ask questions about book content in two modes: full-book question answering and selected-text-only answering. The system will use FastAPI backend with Qdrant vector database for retrieval and OpenAI for response generation, integrated seamlessly into the Docusaurus site.

## Technical Context

**Language/Version**: Python 3.9+ for backend, JavaScript/TypeScript for frontend
**Primary Dependencies**: FastAPI, OpenAI SDK, Qdrant client, Neon Postgres driver, Docusaurus
**Storage**: Qdrant Cloud (vector database), Neon Serverless Postgres (metadata)
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Linux server (backend), Web browsers (frontend)
**Project Type**: Web application with backend API and frontend integration
**Performance Goals**: Response times under 3 seconds, support 100+ concurrent users
**Constraints**: <3s p95 response time, proper hallucination prevention, privacy compliance
**Scale/Scope**: Educational use, 10k+ students, book content indexing

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **RAG Chatbot for Physical AI Book**: Implementation focuses on book-specific interface
- ✅ **Strict Book Content Adherence**: Response generation will be grounded in book content only
- ✅ **Dual Mode Operation**: Both full-book and selected-text modes will be implemented
- ✅ **Grounded Educational Responses**: Responses will cite chapters/modules and be educational
- ✅ **Privacy and Scalability**: Architecture will respect privacy and be scalable
- ✅ **Hallucination Prevention**: System will respond with "This is not covered in the book" when appropriate
- ✅ **Rate Limiting**: Per-user request throttling will be implemented

## Project Structure

### Documentation (this feature)

```text
specs/1-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-contract.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── document.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_service.py
│   │   ├── embedding_service.py
│   │   └── document_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── chat.py
│   │       └── health.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── validation.py
├── scripts/
│   └── ingest_documents.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── ChatWidget/
│   │   │   ├── ChatWidget.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   └── QueryInput.jsx
│   │   └── HighlightHandler/
│   │       └── highlightHandler.js
│   ├── services/
│   │   └── apiService.js
│   └── styles/
│       └── chat.css
└── docusaurus-plugin/
    └── chat-plugin.js

docs/
└── docusaurus/
    └── plugins/
        └── rag-chatbot/
            └── index.js
```

**Structure Decision**: Web application structure chosen with separate backend and frontend to maintain clean separation of concerns. Backend handles RAG logic and API, while frontend provides Docusaurus integration for seamless book reading experience.

## Implementation Phases

### Phase 1: Data Ingestion
- Parse MDX files from book content
- Clean and preprocess text
- Chunk by semantic sections with proper context preservation
- Generate embeddings using OpenAI
- Store in Qdrant with chapter/module metadata
- Index book content for efficient retrieval

### Phase 2: Backend API
- FastAPI server implementation
- `/chat` endpoint supporting both query modes
- Vector retrieval logic with Qdrant
- OpenAI response generation with grounding enforcement
- Session management and metadata storage
- Rate limiting and error handling

### Phase 3: Frontend Integration
- Chat UI component with responsive design
- Highlight-to-query functionality
- API integration with error handling
- Docusaurus plugin for seamless embedding
- Citation display with links to book sections

### Phase 4: Deployment & Production
- Environment variable management
- Production-ready configuration
- Comprehensive error handling and logging
- Performance optimization
- Security hardening

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple data stores | Vector DB for semantic search + relational DB for metadata | Single store insufficient for both vector operations and structured metadata |
| Dual mode complexity | Required by feature specification for different user needs | Single mode would not meet full feature requirements |