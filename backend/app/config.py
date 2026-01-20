from pydantic_settings import BaseSettings
from typing import List, Optional, Dict

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "AI Documentation Backend"
    API_VERSION: str = "1.0.0"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # OpenRouter Configuration (replaces OPENAI_API_KEY)
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "mistralai/devstral-2512:free"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # Cohere Configuration
    COHERE_API_KEY: str
    COHERE_MODEL: str = "command-r-plus-08-2024"
    COHERE_BASE_URL: str = "https://api.cohere.ai/v1"

    # Model Selection Defaults
    DEFAULT_PROVIDER: str = "openrouter"
    DEFAULT_MODEL: str = "mistralai/devstral-2512:free"

    # Available Models
    AVAILABLE_MODELS: Dict[str, List[str]] = {
        "openrouter": ["mistralai/devstral-2512:free"],
        "cohere": ["command-r-plus-08-2024"]
    }

    # Embedding Configuration
    EMBEDDING_MODEL: str = "embed-english-v3.0"

    # Qdrant Configuration
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "documentation"
    QDRANT_VECTOR_SIZE: int = 1024  # Cohere embedding dimension
    QDRANT_DISTANCE_METRIC: str = "Cosine"

    # Database Configuration
    QDRANT_GRPC_ENABLED: bool = True
    QDRANT_TIMEOUT: int = 30

    # Application Settings
    ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",  # Local development frontend
    "http://localhost:8080",
    "http://localhost:8081",
    "https://snazyaseen-book-publish.hf.space",  # Hugging Face deployed frontend
    "https://*.hf.space",                         # Hugging Face wildcard
    "https://book-writing-hackathon.vercel.app/", # Vercel deployment
    "https://*.vercel.app",                        # Vercel wildcard
]


    # Allow all origins in development mode only
    CORS_ALLOW_ALL_ORIGINS: bool = False  # Set to True in development.env
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Performance Settings
    RAG_SEARCH_LIMIT: int = 5
    RAG_SCORE_THRESHOLD: float = 0.0
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    class Config:
        env_file = ".env"
        case_sensitive = True
        # Allow extra fields to avoid validation errors for fields that might be in .env but not defined here
        extra = "ignore"

settings = Settings()