from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from app.config import settings
from app.routes import chat, rag, content, agents, book_chat  # Added agents and book_chat import
from app.utils.logging import setup_logging
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    setup_logging()
    await init_db()
    logging.info("Application started")
    yield
    # Shutdown
    logging.info("Application shutting down")

app = FastAPI(
    title="AI Documentation Backend",
    description="Backend services for AI-powered documentation system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(rag.router, prefix="/api/rag", tags=["rag"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])  # Added agents router
app.include_router(book_chat.router, prefix="/api/book-chat", tags=["book-chat"])  # Book-specific chat router

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Add processing time to response headers
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root():
    return {"message": "AI Documentation Backend API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    logging.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )