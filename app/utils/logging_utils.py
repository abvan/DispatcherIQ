"""
Logging utilities
"""
import logging
from app.config.settings import settings


def setup_logging():
    """Configure logging for the application"""
    log_level = logging.DEBUG if settings.debug else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log"),
        ],
    )
    
    # Set Langchain logging level
    logging.getLogger("langchain").setLevel(logging.INFO)
    logging.getLogger("langgraph").setLevel(logging.INFO)