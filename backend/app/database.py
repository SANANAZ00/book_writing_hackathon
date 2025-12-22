from typing import Optional
import logging
from app.config import settings
from qdrant_client.http.models import Distance, VectorParams

logger = logging.getLogger(__name__)

async def init_db():
    """
    Initialize database connections and ensure Qdrant collection exists
    """
    logger.info("Initializing database connections...")

    # Initialize Qdrant connection and ensure collection exists
    try:
        from qdrant_client import QdrantClient

        logger.info(f"Connecting to Qdrant at: {settings.QDRANT_URL}")
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=settings.QDRANT_GRPC_ENABLED,
            timeout=settings.QDRANT_TIMEOUT
        )

        # Check if collection exists, if not create it
        try:
            collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
            logger.info(f"Connected to existing Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")
            logger.info(f"Collection vectors count: {collection_info.points_count}")
            logger.info(f"Vector size: {collection_info.config.params.vectors.size}")
            logger.info(f"Distance metric: {collection_info.config.params.vectors.distance}")
        except Exception as e:
            # Collection doesn't exist, create it
            logger.info(f"Creating Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")
            logger.info(f"Vector size: {settings.QDRANT_VECTOR_SIZE}, Distance: {settings.QDRANT_DISTANCE_METRIC}")

            # Determine distance metric
            distance_metric = Distance.COSINE
            if settings.QDRANT_DISTANCE_METRIC.upper() == "EUCLID":
                distance_metric = Distance.EUCLID
            elif settings.QDRANT_DISTANCE_METRIC.upper() == "DOT":
                distance_metric = Distance.DOT

            client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=settings.QDRANT_VECTOR_SIZE,
                    distance=distance_metric
                )
            )

            logger.info(f"Created Qdrant collection: {settings.QDRANT_COLLECTION_NAME} with vector size {settings.QDRANT_VECTOR_SIZE} and distance {settings.QDRANT_DISTANCE_METRIC}")

        # Perform a simple test to verify everything is working
        test_points = client.count(collection_name=settings.QDRANT_COLLECTION_NAME)
        logger.info(f"Qdrant collection '{settings.QDRANT_COLLECTION_NAME}' verified. Total points: {test_points.count}")

    except Exception as e:
        logger.error(f"Error initializing Qdrant connection: {str(e)}", exc_info=True)
        raise

    logger.info("Database initialization completed successfully")