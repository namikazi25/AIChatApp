import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from backend.session import get_user_model
from models.gpt import call_gpt
from models.gemini import call_gemini
from models.deepseek import call_deepseek

# Load environment variables
load_dotenv()

# Default model if not specified
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")

# User model preferences
user_models: Dict[str, str] = {}

def set_user_model(user_id: str, model: str) -> None:
    """Set the LLM model for a specific user"""
    user_models[user_id] = model

def get_model_for_user(user_id: str) -> str:
    """Get the model preference for a specific user"""
    # Check if user has a model preference
    if user_id in user_models:
        return user_models[user_id]
    
    # Check if user has a model preference in session
    session_model = get_user_model(user_id)
    if session_model:
        return session_model
    
    # Return default model
    return DEFAULT_MODEL

async def get_llm_response(user_id: str, message: str, memory: List[Dict[str, str]]) -> str:
    """Route the request to the appropriate LLM based on user preference"""
    model = get_model_for_user(user_id)
    
    try:
        if model.startswith("gpt"):
            return await call_gpt(message, memory)
        elif model.startswith("gemini"):
            return await call_gemini(message, memory)
        elif model.startswith("deepseek"):
            return await call_deepseek(message, memory)
        else:
            # Fallback to default model
            return await call_gpt(message, memory)
    except Exception as e:
        # Log the error and fallback to a simple response
        print(f"Error calling LLM: {str(e)}")
        return f"I'm sorry, I encountered an error while processing your request. Please try again later."