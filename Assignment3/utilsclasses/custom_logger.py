import logging

# Configure logging with timestamps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

def log_info(message: str):
    """Logs an informational message with a timestamp."""
    logger.info(message)
