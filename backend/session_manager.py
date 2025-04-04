from typing import Dict, List, Any, Optional, Union
import time
from backend.storage import StorageBackend, MemoryStorage

class SessionManager:
    def __init__(self, storage_backend: StorageBackend = None, max_memory_size: int = 20, session_timeout: int = 7200):
        # Use memory storage by default if no storage backend is provided
        self.storage = storage_backend or MemoryStorage()
        self.MAX_MEMORY_SIZE = max_memory_size
        self.SESSION_TIMEOUT = session_timeout
    
    def get_session_key(self, user_id: str, context_id: Optional[str] = None) -> str:
        """Generate a session key from user_id and optional context_id
        
        Args:
            user_id: The Discord user ID
            context_id: Optional context ID (thread_id or dm_channel_id)
            
        Returns:
            A composite session key
        """
        if context_id:
            return f"{user_id}:{context_id}"
        return user_id
    
    def get_memory(self, user_id: str, context_id: Optional[str] = None) -> List[Dict[str, str]]:
        """Get the chat history for a specific session
        
        Args:
            user_id: The Discord user ID
            context_id: Optional context ID (thread_id or dm_channel_id)
            
        Returns:
            The chat history for the specified session
        """
        # Generate session key
        session_key = self.get_session_key(user_id, context_id)
        
        # Get session from storage
        session = self.storage.get(session_key)
        
        # Create session if it doesn't exist
        if not session:
            session = {
                "messages": [],
                "model": None,
                "last_activity": time.time()
            }
            self.storage.set(session_key, session)
        else:
            # Update last activity timestamp
            session["last_activity"] = time.time()
            self.storage.set(session_key, session)
        
        return session["messages"]
    
    def add_to_memory(self, user_id: str, message: Dict[str, str], context_id: Optional[str] = None) -> None:
        """Add a message to the session's chat history
        
        Args:
            user_id: The Discord user ID
            message: The message to add to the chat history
            context_id: Optional context ID (thread_id or dm_channel_id)
        """
        # Generate session key
        session_key = self.get_session_key(user_id, context_id)
        
        # Get session from storage
        session = self.storage.get(session_key)
        
        # Create session if it doesn't exist
        if not session:
            session = {
                "messages": [],
                "model": None,
                "last_activity": time.time()
            }
        
        # Add message to memory
        session["messages"].append(message)
        
        # Update last activity timestamp
        session["last_activity"] = time.time()
        
        # Trim memory if it exceeds the maximum size
        if len(session["messages"]) > self.MAX_MEMORY_SIZE:
            # Remove oldest messages, but keep system messages
            system_messages = [msg for msg in session["messages"] if msg["role"] == "system"]
            other_messages = [msg for msg in session["messages"] if msg["role"] != "system"]
            
            # Keep only the most recent messages
            other_messages = other_messages[-(self.MAX_MEMORY_SIZE - len(system_messages)):]
            
            # Combine system messages with recent messages
            session["messages"] = system_messages + other_messages
        
        # Save session to storage
        self.storage.set(session_key, session)
    
    def get_user_model(self, user_id: str, context_id: Optional[str] = None) -> str:
        """Get the model preference for a specific session
        
        Args:
            user_id: The Discord user ID
            context_id: Optional context ID (thread_id or dm_channel_id)
            
        Returns:
            The model preference for the specified session or default
        """
        # Generate session key
        session_key = self.get_session_key(user_id, context_id)
        
        # Get session from storage
        session = self.storage.get(session_key)
        
        # Create session if it doesn't exist
        if not session:
            session = {
                "messages": [],
                "model": None,
                "last_activity": time.time()
            }
            self.storage.set(session_key, session)
        
        # Return user's model preference or default
        return session.get("model", "gpt-4o")
    
    def set_user_model(self, user_id: str, model: str, context_id: Optional[str] = None) -> None:
        """Set the model preference for a specific session
        
        Args:
            user_id: The Discord user ID
            model: The model to set as preference
            context_id: Optional context ID (thread_id or dm_channel_id)
        """
        # Generate session key
        session_key = self.get_session_key(user_id, context_id)
        
        # Get session from storage
        session = self.storage.get(session_key)
        
        # Create session if it doesn't exist
        if not session:
            session = {
                "messages": [],
                "model": None,
                "last_activity": time.time()
            }
        
        # Set model preference
        session["model"] = model
        
        # Update last activity timestamp
        session["last_activity"] = time.time()
        
        # Save session to storage
        self.storage.set(session_key, session)
    
    def cleanup_sessions(self) -> int:
        """Remove inactive sessions to free up memory
        
        Returns:
            The number of inactive sessions removed
        """
        current_time = time.time()
        inactive_sessions = []
        
        # Get all sessions
        all_sessions = self.storage.get_all()
        
        # Find inactive sessions
        for session_key, session in all_sessions.items():
            if current_time - session["last_activity"] > self.SESSION_TIMEOUT:
                inactive_sessions.append(session_key)
        
        # Remove inactive sessions
        for session_key in inactive_sessions:
            self.storage.delete(session_key)
        
        return len(inactive_sessions)