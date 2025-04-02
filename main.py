import os
import asyncio
import uvicorn
import threading
from dotenv import load_dotenv
from bot.client import run_bot
from utils.logger import get_logger

# Load environment variables
load_dotenv()

# Set up logger
logger = get_logger("main")

def run_backend():
    """Run the FastAPI backend"""
    logger.info("Starting FastAPI backend...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, log_level="info")

def run_discord_bot():
    """Run the Discord bot"""
    logger.info("Starting Discord bot...")
    run_bot()

def main():
    """Run both the Discord bot and FastAPI backend"""
    logger.info("Starting Discord LLM Bot application...")
    
    # Check if environment variables are set
    required_vars = ["DISCORD_BOT_TOKEN", "OPENAI_API_KEY", "GOOGLE_API_KEY", "DEEPSEEK_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file and try again.")
        return
    
    # Start the FastAPI backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Run the Discord bot in the main thread
    run_discord_bot()

if __name__ == "__main__":
    main()