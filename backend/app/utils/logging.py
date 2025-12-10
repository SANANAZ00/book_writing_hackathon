import logging
import sys
from app.config import settings

def setup_logging():
    """
    Set up logging configuration
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Clear existing handlers and add our console handler
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    # Set specific log levels for libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("qdrant_client").setLevel(logging.INFO)
    logging.getLogger("openai").setLevel(logging.INFO)