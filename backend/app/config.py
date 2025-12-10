from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "AI Documentation Backend"
    API_VERSION: str = "1.0.0"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"

    # Qdrant Configuration
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "documentation"

    # Database Configuration
    QDRANT_GRPC_ENABLED: bool = True
    QDRANT_TIMEOUT: int = 30

    # Application Settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
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