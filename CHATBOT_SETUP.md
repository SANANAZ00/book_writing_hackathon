# Lucy AI Assistant - Deployment and Configuration Guide

## Environment Variables

Create a `.env` file in the root of your frontend project with the following variables:

```env
# Backend API URL - Replace with your deployed backend URL on Hugging Face
REACT_APP_BACKEND_URL=https://your-huggingface-space-name.hf.space
# Alternative environment variable name (for Vercel deployments)
NEXT_PUBLIC_BACKEND_URL=https://your-huggingface-space-name.hf.space

# Additional configuration
REACT_APP_DEBUG=true
```

## API Endpoints Used

- Health Check: `GET /health`
- Book Chat: `POST /api/book-chat/`
- Book Chat Health: `GET /api/book-chat/health`

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Ensure your backend allows requests from your frontend domain
2. **Connection Status Shows Offline**:
   - Verify your backend URL is correct
   - Check that your backend is running and accessible
   - Confirm the health endpoint is responding
3. **Messages Not Sending**:
   - Check network tab in browser dev tools
   - Verify backend is receiving requests
   - Confirm API endpoint is correct

### Backend Requirements:

Your backend must have the following endpoints available:
- `/health` - Returns health status of the backend
- `/api/book-chat/` - Handles chat requests with RAG capabilities
- `/api/book-chat/health` - Returns health status of book chat service

### Frontend Configuration:

The frontend will try environment variables in this order:
1. `REACT_APP_BACKEND_URL`
2. `NEXT_PUBLIC_BACKEND_URL`
3. Falls back to placeholder URL

## Testing the Connection

1. Open the chat interface
2. Check the connection status indicator in the header
3. Use the refresh button (🔄) to manually check connection
4. Send a test message to verify full functionality

## API Request Format

When sending messages, the frontend sends:
```json
{
  "message": "user input",
  "selected_text": "optional selected text",
  "mode": "full_book|selected_text",
  "session_id": "optional session id",
  "provider": "cohere",
  "model": "command-r-plus-08-2024",
  "temperature": 0.7,
  "max_tokens": 500,
  "search_limit": 5,
  "score_threshold": 0.3,
  "history": [{"role": "user|assistant", "content": "message content"}]
}
```

## Response Format Expected

The backend should respond with:
```json
{
  "response": "AI response text",
  "sources": [{"title": "source title", "content": "source content", ...}],
  "session_id": "session identifier",
  "model_used": "model name",
  "provider": "provider name",
  "usage": {"tokens_used": 123}
}
```