import logging
import sys
from app.config import settings

def setup_logging():
    """
    Set up comprehensive logging configuration
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)

    # Create detailed formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Clear existing handlers and add our console handler
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    # Set specific log levels for libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    logging.getLogger("fastapi").setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    logging.getLogger("qdrant_client").setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    logging.getLogger("openai").setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    logging.getLogger("cohere").setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)

    # Reduce noise from HTTP libraries
    logging.getLogger("httpx").setLevel(logging.WARNING if not settings.DEBUG else logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING if not settings.DEBUG else logging.DEBUG)
    logging.getLogger("httpcore").setLevel(logging.WARNING if not settings.DEBUG else logging.DEBUG)

    logging.info("Logging configuration initialized")