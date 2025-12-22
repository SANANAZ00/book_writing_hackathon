from pydantic_settings import BaseSettings
from typing import List, Optional, Dict

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "AI Documentation Backend"
    API_VERSION: str = "1.0.0"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"  # Default OpenAI model
    EMBEDDING_MODEL: str = "embed-english-v3.0"  # Cohere embedding model
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    # Cohere Configuration
    COHERE_API_KEY: str
    COHERE_MODEL: str = "command-r-plus-08-2024"  # Cohere chat model (command-r was removed)
    COHERE_BASE_URL: str = "https://api.cohere.ai/v1"

    # Model Selection Defaults
    DEFAULT_PROVIDER: str = "cohere"
    DEFAULT_MODEL: str = "command-r-plus-08-2024"

    # Available Models
    AVAILABLE_MODELS: Dict[str, List[str]] = {
        "openai": ["gpt-4o-mini", "gpt-4o"],
        "cohere": ["command-r-plus-08-2024"]
    }

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
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:3001", "https://*.vercel.app"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Performance Settings
    RAG_SEARCH_LIMIT: int = 5
    RAG_SCORE_THRESHOLD: float = 0.3
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()