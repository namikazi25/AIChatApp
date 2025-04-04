from typing import Dict, List, Any, Optional, Tuple
import time
from backend.storage import MemoryStorage
from backend.session_manager import SessionManager

# Maximum number of messages to keep in memory per session
MAX_MEMORY_SIZE = 20

# Session timeout in seconds (2 hours)
SESSION_TIMEOUT = 7200

# Create a global session manager with in-memory storage
# This can be replaced with database storage in the future
_session_manager = SessionManager(MemoryStorage(), MAX_MEMORY_SIZE, SESSION_TIMEOUT)

def get_session_key(user_id: str, context_id: Optional[str] = None) -> str:
    """Generate a session key from user_id and optional context_id
    
    Args:
        user_id: The Discord user ID
        context_id: Optional context ID (thread_id or dm_channel_id)
        
    Returns:
        A composite session key
    """
    return _session_manager.get_session_key(user_id, context_id)

def get_memory(user_id: str, context_id: Optional[str] = None) -> List[Dict[str, str]]:
    """Get the chat history for a specific session
    
    Args:
        user_id: The Discord user ID
        context_id: Optional context ID (thread_id or dm_channel_id)
        
    Returns:
        The chat history for the specified session
    """
    return _session_manager.get_memory(user_id, context_id)

def add_to_memory(user_id: str, message: Dict[str, str], context_id: Optional[str] = None) -> None:
    """Add a message to the session's chat history
    
    Args:
        user_id: The Discord user ID
        message: The message to add to the chat history
        context_id: Optional context ID (thread_id or dm_channel_id)
    """
    _session_manager.add_to_memory(user_id, message, context_id)

def get_user_model(user_id: str, context_id: Optional[str] = None) -> str:
    """Get the model preference for a specific session
    
    Args:
        user_id: The Discord user ID
        context_id: Optional context ID (thread_id or dm_channel_id)
        
    Returns:
        The model preference for the specified session or default
    """
    return _session_manager.get_user_model(user_id, context_id)

def set_user_model(user_id: str, model: str, context_id: Optional[str] = None) -> None:
    """Set the model preference for a specific session
    
    Args:
        user_id: The Discord user ID
        model: The model to set as preference
        context_id: Optional context ID (thread_id or dm_channel_id)
    """
    _session_manager.set_user_model(user_id, model, context_id)

def cleanup_sessions() -> int:
    """Remove inactive sessions to free up memory
    
    Returns:
        The number of inactive sessions removed
    """
    return _session_manager.cleanup_sessions()

# Function to change the storage backend
def set_storage_backend(storage_backend) -> None:
    """Change the storage backend for the session manager
    
    Args:
        storage_backend: The new storage backend to use
    """
    global _session_manager
    _session_manager = SessionManager(storage_backend, MAX_MEMORY_SIZE, SESSION_TIMEOUT)