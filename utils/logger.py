import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Set up logging format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create a formatter
formatter = logging.Formatter(log_format)

# Create a file handler that logs to a file with the current date
log_file = f"logs/discord_bot_{datetime.now().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

# Create a stream handler that logs to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

def get_logger(name):
    """Get a logger with the specified name"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Add handlers if they haven't been added already
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger

# Create loggers for different components
bot_logger = get_logger("bot")
backend_logger = get_logger("backend")
models_logger = get_logger("models")
utils_logger = get_logger("utils")