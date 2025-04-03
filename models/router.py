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
    from backend.session import set_user_model as session_set_user_model
    user_models[user_id] = model
    session_set_user_model(user_id, model)  # Sync with session storage

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

# models/router.py - Add validation
VALID_MODELS = {
    "gpt-4o": call_gpt,
    "gemini-2.0-flash": lambda m, mem: call_gemini(m, mem, "gemini-2.0-flash"),
    "gemini-2.5-pro-experimental": lambda m, mem: call_gemini(m, mem, "gemini-2.5-pro-experimental"),
    "deepseek-v3": call_deepseek
}


async def get_llm_response(user_id: str, message: str, memory: List[Dict[str, str]]) -> str:
    """Route the request to the appropriate LLM based on user preference"""
    model = get_model_for_user(user_id)
    
    try:
        if model == "gpt-4o":
            return await call_gpt(message, memory)
        elif model == "gemini-2.0-flash":
            return await call_gemini(message, memory, model="gemini-2.0-flash")
        elif model == "gemini-2.5-pro-experimental":
            return await call_gemini(message, memory, model="gemini-2.5-pro-experimental")
        elif model == "deepseek-v3":
            return await call_deepseek(message, memory)
        else:
            # Fallback to default model
            return await call_gpt(message, memory)
    except Exception as e:
        print(f"Error calling LLM: {str(e)}")
        return f"I'm sorry, I encountered an error while processing your request. Please try again later."