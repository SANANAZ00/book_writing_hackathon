# Data Model for RAG Chatbot

## Entity: Chat Session
- **session_id**: string (unique identifier)
- **user_id**: string (optional, for logged-in users)
- **created_at**: datetime
- **last_accessed**: datetime
- **mode**: enum (full_book, selected_text)
- **metadata**: object (additional session data)

## Entity: User Query
- **query_id**: string (unique identifier)
- **session_id**: string (foreign key to Chat Session)
- **query_text**: string (the user's question)
- **mode**: enum (full_book, selected_text)
- **selected_text**: string (optional, for selected-text mode)
- **timestamp**: datetime
- **metadata**: object (query context)

## Entity: Book Content Chunk
- **chunk_id**: string (unique identifier)
- **document_id**: string (identifier for the source document)
- **content**: string (the text content)
- **embedding**: array<float> (vector embedding)
- **metadata**: object (source chapter/module, page range, etc.)
- **created_at**: datetime

## Entity: Response
- **response_id**: string (unique identifier)
- **query_id**: string (foreign key to User Query)
- **response_text**: string (the generated response)
- **sources**: array<object> (citations to book sections)
- **confidence**: float (confidence level of the response)
- **timestamp**: datetime
- **metadata**: object (additional response data)

## Entity: Book Metadata
- **chapter_id**: string (unique identifier)
- **title**: string (chapter title)
- **section**: string (section name)
- **page_range**: string (page range in book)
- **embedding_model**: string (model used for embeddings)
- **created_at**: datetime
- **updated_at**: datetime