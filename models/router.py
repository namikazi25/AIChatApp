import os
from typing import Dict, List, Any, Optional
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

def set_user_model(user_id: str, model: str, context_id: Optional[str] = None) -> None:
    """Set the LLM model for a specific user"""
    from backend.session import set_user_model as session_set_user_model
    session_key = f"{user_id}:{context_id}" if context_id else user_id
    user_models[session_key] = model
    session_set_user_model(user_id, model, context_id)  # Sync with session storage

def get_model_for_user(user_id: str, context_id: Optional[str] = None) -> str:
    """Get the model preference for a specific user"""
    # Generate session key
    session_key = f"{user_id}:{context_id}" if context_id else user_id
    
    # Check if user has a model preference
    if session_key in user_models:
        return user_models[session_key]
    
    # Check if user has a model preference in session
    session_model = get_user_model(user_id, context_id)
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


async def get_llm_response(user_id: str, message: str, memory: List[Dict[str, str]], context_id: Optional[str] = None) -> str:
    """Route the request to the appropriate LLM based on user preference"""
    model = get_model_for_user(user_id, context_id)
    
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