# Physical AI & Humanoid Robotics - Book Information

## Book Details

**Title:** Physical AI & Humanoid Robotics

**Project Name:** physical-ai-robotics

**Repository:** https://github.com/SANANAZ00/book_writing_hackathon

## Where the Book is Written

The book content is organized in the following directory structure:

### Documentation Structure
- **Main Docs Directory:** `/docs/`
  - **Foundations:** `/docs/foundations/` - Core concepts and fundamentals
    - `ai-powered-documentation.mdx`
    - `claude-code.mdx`
    - `docusaurus-fundamentals.mdx`
    - `openai-integration.mdx`
    - `qdrant-cloud.mdx`
    - `rag-systems.mdx`
    - `spec-driven-development.mdx`
  
  - **Systems:** `/docs/systems/` - Advanced systems and implementations
    - `building-rag-chatbot.mdx`
    - `content-generation.mdx`
    - `environment-setup.mdx`
    - `fastapi-backend.mdx`
  
  - **Design:** `/docs/design/` - Design patterns and principles
  
  - **Mastery:** `/docs/mastery/` - Advanced topics
  
  - **Meta:** `/docs/meta/` - Meta documentation
  
  - **Templates:** `/docs/templates/` - Content templates

### Blog Posts
- **Blog Directory:** `/blog/`
  - Various blog posts in Markdown and MDX format

### Introduction
- **Entry Point:** `/docs/intro.md` - Main introduction to the book

## Book Configuration Files

### Configuration Files
- **`docusaurus.config.js`** - Main Docusaurus configuration
- **`sidebars.js`** - Navigation sidebar configuration
- **`package.json`** - Project dependencies and scripts

### Theme & Components
- **`src/theme/`** - Custom theme components
  - `Layout.js` - Main layout wrapper
  - `DocItem/` - Document item customization
  - `MDXComponents.js` - Custom MDX components
  
- **`src/components/`** - Custom React components
  - `ChatbotWidget.js` - AI chatbot integration
  - `CalloutBox.js` - Content callout boxes
  - `ConceptCard.js` - Concept cards
  - `PageHeader.js` - Page headers
  - `StepFlow.js` - Step-by-step flows
  - `MiniMap.js` - Content minimap
  - `ResponsiveDesign.js` - Responsive design utilities

### Styling
- **`src/css/custom.css`** - Custom CSS styles

## Backend Integration

The book includes an integrated backend for AI features:

- **Backend Directory:** `/backend/`
  - **Main App:** `/backend/app/`
    - `main.py` - FastAPI application entry point
    - `config.py` - Configuration settings
    - `database.py` - Database setup
  
  - **Agents:** `/backend/app/agents/` - AI agents
    - `base.py`
    - `content_expansion.py`
    - `deployment_helper.py`
    - `manager.py`
    - `qdrant_data.py`
    - `rag_optimization.py`
    - `skills.py`
    - `ui_ux_refinement.py`
  
  - **Routes:** `/backend/app/routes/` - API endpoints
    - `agents.py`
    - `chat.py`
    - `content.py`
    - `rag.py`
  
  - **Utils:** `/backend/app/utils/` - Utility functions
  
  - **Scripts:** `/backend/scripts/` - Maintenance scripts

## Building and Running

### Development Server
```bash
npm start
```
Runs the development server at `http://localhost:3000`

### Production Build
```bash
npm run build
```
Creates an optimized production build

### Other Commands
- `npm run deploy` - Deploy to GitHub Pages
- `npm run clear` - Clear build cache
- `npm run serve` - Serve production build locally

## Publishing

- **URL:** https://sananaz00.github.io/book_writing_hackathon/
- **GitHub Pages:** Enabled for this repository
- **Base URL:** `/book_writing_hackathon/`

## Book Status

The book is currently in active development with content being written and expanded in the documentation directories listed above.

---

Last Updated: December 10, 2025
