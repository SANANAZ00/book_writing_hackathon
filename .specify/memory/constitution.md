<!--
Sync Impact Report:
Version change: 0.2.0 → 1.0.0
List of modified principles:
  - Physical AI Focus → RAG Chatbot for Physical AI Book
  - ROS 2 Integration → Strict Book Content Adherence
  - Simulation Mastery → Dual Mode Operation
  - NVIDIA Isaac Integration → Grounded Educational Responses
  - Humanoid Robotics Focus → Privacy and Scalability
  - Vision-Language-Action Integration → Removed
Added sections: Technology Stack for RAG Chatbot, Backend Architecture, Frontend Integration
Removed sections: Previous Physical AI book content, Modules, Technical Stack (old)
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/sp.phr.md ⚠ pending
Follow-up TODOs: None
-->
# RAG Chatbot for Physical AI & Humanoid Robotics Book Constitution

The RAG (Retrieval-Augmented Generation) chatbot for "Physical AI & Humanoid Robotics" provides an intelligent interface for students and researchers to interact with the book content. The system retrieves relevant passages from the book and generates accurate, educational responses based strictly on the book's content.

## Core Principles

### RAG Chatbot for Physical AI Book
The system MUST serve as an intelligent interface specifically for the "Physical AI & Humanoid Robotics" book. All functionality MUST be designed around enhancing the user's interaction with the book content, enabling deep understanding of Physical AI and humanoid robotics concepts.

### Strict Book Content Adherence
The chatbot MUST answer strictly from the book content unless explicitly instructed otherwise. The system MUST NOT generate responses based on general knowledge or external sources when the query relates to the book topic. If information is not covered in the book, respond with "This is not covered in the book."

### Dual Mode Operation
The chatbot MUST support two operational modes: (1) Full-book question answering for comprehensive queries, and (2) Selected-text-only answering for user-highlighted text. Both modes MUST maintain strict adherence to the book content.

### Grounded Educational Responses
All answers MUST be grounded, concise, and educational. The system MUST cite chapter/module titles when possible to guide users to relevant sections. Responses MUST be pedagogically sound, supporting the learning objectives of the Physical AI course.

### Privacy and Scalability
The system MUST respect user privacy and not store chat logs unless explicitly required for functionality. The architecture MUST be scalable and modular, supporting potential growth in users and content while maintaining performance and security.

## Architecture and Technical Stack

### Executive Summary
The RAG chatbot integrates with the Physical AI book content to provide contextual, intelligent responses. The system combines vector retrieval from Qdrant Cloud with generative responses from OpenAI models, all orchestrated through a FastAPI backend and integrated into Docusaurus frontend.

### Technology Stack for RAG Chatbot
- **Backend**: FastAPI for RESTful API endpoints
- **LLM**: OpenAI Agents / ChatKit SDK for response generation
- **Vector Database**: Qdrant Cloud (Free Tier) for content indexing and retrieval
- **Metadata Store**: Neon Serverless Postgres for session and metadata management
- **Frontend**: Docusaurus integration for seamless book reading experience
- **Embeddings**: Text embeddings for semantic similarity matching

### Backend Architecture
- **API Endpoints**: `/chat`, `/rag-query`, `/mode-switch`
- **Authentication**: Session-based or JWT if required
- **Rate Limiting**: Per-user request throttling
- **Error Handling**: Comprehensive error responses with appropriate HTTP codes
- **Logging**: Structured logging for debugging and monitoring

### Frontend Integration
- **UI Components**: Chat interface within Docusaurus pages
- **Text Selection**: Highlight-to-query functionality for selected-text-only mode
- **Response Display**: Formatted responses with citations to book chapters
- **Mode Toggle**: Clear switching between full-book and selected-text modes

### Data Models
- **Chat Session**: `{session_id, user_id, created_at, last_accessed}`
- **Query Log**: `{query_id, session_id, query_text, response, timestamp, mode}`
- **Document Chunk**: `{chunk_id, document_id, content, embedding, metadata}`
- **Book Metadata**: `{chapter_id, title, section, page_range, embedding_model}`

### API-Style Specifications for Chatbot
- `POST /chat`:
    - **Input**: `{ "message": "string", "session_id": "string", "mode": "full_book|selected_text", "selected_text": "optional string" }`
    - **Output**: `{ "response": "string", "sources": [{"chapter": "string", "page": "number"}], "session_id": "string" }`
    - **Errors**: 400 (Invalid Request), 429 (Rate Limited), 500 (Processing Error).
- `GET /sessions/{session_id}`:
    - **Input**: Session ID
    - **Output**: `{ "messages": [{"role": "user|assistant", "content": "string", "timestamp": "datetime"}] }`

### UI/UX Guidelines
The interface MUST be intuitive and non-disruptive to the reading experience. Response formatting MUST clearly distinguish between chatbot output and book content. Citation links MUST enable users to jump directly to referenced sections.

## Assessment and Evaluation Framework

### Quality Metrics
- **Accuracy**: Percentage of responses that correctly cite book content
- **Relevance**: User satisfaction with response applicability to their query
- **Grounding**: Percentage of responses that can be traced to specific book sections
- **Performance**: Response times under acceptable thresholds

### Testing Framework
- **Unit Tests**: Individual components (embedding, retrieval, response generation)
- **Integration Tests**: Full query-response pipeline validation
- **Content Validation**: Ensuring responses are properly grounded in book content
- **Load Tests**: Performance under expected user concurrency

## Implementation Requirements

### Content Quality Standards
- **Fidelity**: Responses MUST accurately reflect book content without distortion
- **Clarity**: Responses MUST be clear and educational, appropriate for target audience
- **Consistency**: Behavior MUST be consistent across both operational modes
- **Citation Accuracy**: Source references MUST correctly point to actual book sections

### Technical Requirements
- **Scalability**: Architecture MUST support concurrent users efficiently
- **Reliability**: System MUST maintain high availability for educational use
- **Security**: User data MUST be protected according to privacy principles
- **Maintainability**: Codebase MUST follow clean architecture principles

### Performance Benchmarks
- **Response Time**: Under 3 seconds for typical queries
- **Availability**: 99% uptime during academic periods
- **Throughput**: Support 100+ concurrent users during peak times

## Constraints, Risks, and Edge Cases

### Content Scope
The chatbot MUST remain focused solely on the Physical AI & Humanoid Robotics book content. No general AI knowledge, external resources, or unrelated topics are permitted in responses.

### Hallucination Prevention
The system MUST implement safeguards against generating information not present in the book. Robust fallback mechanisms MUST respond with "This is not covered in the book" when appropriate.

### Data Privacy
User queries and conversations MUST NOT be stored unnecessarily. Any required storage MUST comply with privacy regulations and institutional policies.

### Rate Limiting
The system MUST implement appropriate rate limiting to prevent abuse while supporting legitimate educational usage.

## Governance
This Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan. All PRs/reviews MUST verify compliance. Complexity MUST be justified.

**Version**: 1.0.0 | **Ratified**: 2025-12-20 | **Last Amended**: 2025-12-20