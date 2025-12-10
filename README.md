# Physical AI & Humanoid Robotics

This project is an AI-powered documentation system that combines Docusaurus for content management with a RAG (Retrieval-Augmented Generation) chatbot for intelligent querying of the documentation.

## Features

- **AI-Powered Documentation**: Intelligent system that understands and responds to natural language queries
- **RAG Chatbot**: Context-aware responses based on documentation content
- **Interactive Learning**: Smart learning journey with dual modes (Beginner/Deep Dive)
- **Subagents & Skills**: Reusable intelligence with dynamic skill loading
- **Responsive Design**: Mobile-friendly interface with smooth UX

## Architecture

The system consists of:

- **Frontend**: Docusaurus-based documentation site with React components
- **Backend**: FastAPI server handling API requests and business logic
- **AI Services**: OpenAI integration for content generation and chat functionality
- **Vector Database**: Qdrant Cloud for semantic search and RAG operations
- **Deployment**: GitHub Pages for frontend, cloud platform for backend

## Prerequisites

- Node.js 18+ for frontend
- Python 3.9+ for backend
- OpenAI API key
- Qdrant Cloud account

## Local Development

### Frontend (Docusaurus)

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) to view the site in the browser.

### Backend (FastAPI)

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Create .env file in backend directory
   echo "OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key" > backend/.env
   ```

4. Start the backend server:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

## Deployment

### Frontend to GitHub Pages

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The GitHub Actions workflow handles the build and deployment process.

### Backend to Cloud Platform

Deploy the FastAPI backend to your preferred cloud platform (Render, Railway, Fly.io, etc.) with the following configuration:

- Environment variables: `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`
- Python runtime 3.9+
- Dependencies from `backend/requirements.txt`

## Project Structure

```
.
├── docs/                   # Docusaurus documentation content
├── src/                    # Custom React components and theme
│   ├── components/         # Reusable UI components
│   └── theme/              # Docusaurus theme customization
├── backend/                # FastAPI backend services
│   ├── app/               # Application code
│   ├── agents/            # Subagents and skills system
│   └── scripts/           # Utility scripts
├── .github/workflows/     # GitHub Actions workflows
└── README.md
```

## Key Components

### Custom Components
- `CalloutBox`: Styled information boxes for tips, warnings, examples
- `ConceptCard`: Standalone knowledge snippets
- `StepFlow`: Interactive step-by-step instructions
- `ChatbotWidget`: Floating AI assistant
- `SelectTextOverlay`: Contextual "Ask AI" button for selected text

### AI Features
- **RAG System**: Semantic search and context-aware responses
- **Subagents**: Specialized AI assistants (UI/UX, Content, RAG, etc.)
- **Skills**: Reusable AI capabilities (explain, rewrite, generate, etc.)
- **Dual Learning Modes**: Beginner and Deep Dive content presentation

## Technologies Used

- **Frontend**: Docusaurus, React, MDX
- **Backend**: FastAPI, Python
- **AI Services**: OpenAI API
- **Vector Database**: Qdrant Cloud
- **Deployment**: GitHub Pages, Cloud platforms
- **Styling**: Infima, custom CSS

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.