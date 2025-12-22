# Research for RAG Chatbot Implementation

## Decision: Technology Stack
**Rationale**: Based on the feature specification and constitution, the technology stack has been defined as:
- Backend: FastAPI
- LLM: OpenAI Agents / ChatKit SDK
- Vector Database: Qdrant Cloud (Free Tier)
- Metadata Store: Neon Serverless Postgres
- Frontend: Docusaurus integration

## Decision: Document Processing Pipeline
**Rationale**: MDX files need to be parsed, cleaned, and chunked by semantic sections before generating embeddings. This approach ensures proper context preservation while maintaining semantic meaning.

## Decision: Chunking Strategy
**Rationale**: Semantic chunking by sections/chapters is optimal for book content as it maintains context while enabling precise retrieval. This aligns with the requirement to cite specific chapters/modules.

## Decision: Dual Mode Implementation
**Rationale**: Two operational modes (full-book and selected-text) are required per the feature specification. This requires different retrieval strategies - full-book for comprehensive queries and selected-text for focused queries.

## Decision: Rate Limiting Strategy
**Rationale**: Per-user request throttling is necessary to prevent abuse while supporting legitimate educational usage, as specified in the constitution.

## Decision: Privacy and Data Handling
**Rationale**: Following the constitution's privacy requirements, chat logs will not be stored unnecessarily, and only essential session metadata will be retained.