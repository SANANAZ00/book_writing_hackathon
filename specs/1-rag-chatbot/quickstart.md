# Quickstart Guide for RAG Chatbot

## Prerequisites
- Python 3.9+
- Docker (for local development)
- Qdrant Cloud account
- Neon Postgres account
- OpenAI API key

## Setup

### 1. Clone and Install Dependencies
```bash
git clone [repository-url]
cd [repository-name]
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file with the following:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_connection_string
```

### 3. Initialize Vector Database
```bash
# Process MDX files and populate Qdrant
python -m scripts.ingest_documents
```

### 4. Start Backend Server
```bash
# Start FastAPI server
uvicorn backend.main:app --reload --port 8000
```

### 5. Frontend Integration
The chat widget is designed to be embedded in Docusaurus pages. Include the widget component in your Docusaurus theme configuration.

## Usage
1. Navigate to the book page in Docusaurus
2. Access the chat interface
3. Ask questions about book content or select text for focused queries
4. Receive responses with citations to relevant chapters/modules

## Development
- Backend API endpoints available at http://localhost:8000
- API documentation available at http://localhost:8000/docs
- Frontend components in the `frontend/` directory