---
id: 1
title: "Update Constitution RAG Chatbot"
stage: "constitution"
date_iso: "2025-12-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "rag-chatbot", "physical-ai"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt

```
This constitution governs the RAG chatbot for the book "Physical AI & Humanoid Robotics".

Principles:
- The chatbot MUST answer strictly from the book content unless explicitly instructed otherwise.
- The chatbot MUST support two modes:
  1. Full-book question answering
  2. Selected-text-only answering (user-highlighted text)
- All answers MUST be grounded, concise, and educational.
- No hallucinations: if information is missing, respond with "This is not covered in the book."
- Cite chapter/module titles when possible.
- Respect user privacy and do not store chat logs unless explicitly required.
- System must be scalable and modular.

Technology Constraints:
- Backend: FastAPI
- LLM: OpenAI Agents / ChatKit SDK
- Vector DB: Qdrant Cloud (Free Tier)
- Metadata store: Neon Serverless Postgres
- Frontend integration inside Docusaurus
```

# Response

Updated the project constitution to reflect the RAG chatbot for the Physical AI & Humanoid Robotics book. The new constitution includes:

- Core principles aligned with the specified requirements
- Architecture and technical stack details
- Implementation requirements
- Quality standards and evaluation framework
- Privacy and scalability considerations

The constitution is now properly configured for the RAG chatbot project with all specified constraints and principles.

# Outcome

The constitution has been successfully updated and saved to `.specify/memory/constitution.md` with version 1.0.0, reflecting all the required principles for the RAG chatbot project.

# Evaluation

The updated constitution meets all the specified requirements:
- ✅ Chatbot answers strictly from book content
- ✅ Supports dual mode operation (full-book and selected-text)
- ✅ Ensures grounded, educational responses
- ✅ Prevents hallucinations with proper fallback
- ✅ Includes citation requirements
- ✅ Respects user privacy
- ✅ Designed for scalability and modularity
- ✅ Incorporates all technology constraints