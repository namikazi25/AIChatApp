from typing import Dict, List, Any
import time

# In-memory storage for user sessions
# Format: {user_id: {"messages": [...], "model": "...", "last_activity": timestamp}}
user_sessions: Dict[str, Dict[str, Any]] = {}

# Maximum number of messages to keep in memory per user
MAX_MEMORY_SIZE = 20

# Session timeout in seconds (2 hours)
SESSION_TIMEOUT = 7200

def get_memory(user_id: str) -> List[Dict[str, str]]:
    """Get the chat history for a specific user"""
    # Create session if it doesn't exist
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "messages": [],
            "model": None,
            "last_activity": time.time()
        }
    else:
        # Update last activity timestamp
        user_sessions[user_id]["last_activity"] = time.time()
    
    return user_sessions[user_id]["messages"]

def add_to_memory(user_id: str, message: Dict[str, str]) -> None:
    """Add a message to the user's chat history"""
    # Create session if it doesn't exist
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "messages": [],
            "model": None,
            "last_activity": time.time()
        }
    
    # Add message to memory
    user_sessions[user_id]["messages"].append(message)
    
    # Update last activity timestamp
    user_sessions[user_id]["last_activity"] = time.time()
    
    # Trim memory if it exceeds the maximum size
    if len(user_sessions[user_id]["messages"]) > MAX_MEMORY_SIZE:
        # Remove oldest messages, but keep system messages
        system_messages = [msg for msg in user_sessions[user_id]["messages"] if msg["role"] == "system"]
        other_messages = [msg for msg in user_sessions[user_id]["messages"] if msg["role"] != "system"]
        
        # Keep only the most recent messages
        other_messages = other_messages[-(MAX_MEMORY_SIZE - len(system_messages)):]
        
        # Combine system messages with recent messages
        user_sessions[user_id]["messages"] = system_messages + other_messages

def get_user_model(user_id: str) -> str:
    """Get the model preference for a specific user"""
    # Create session if it doesn't exist
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "messages": [],
            "model": None,
            "last_activity": time.time()
        }
    
    # Return user's model preference or default
    return user_sessions[user_id].get("model", "gpt-4o")

def set_user_model(user_id: str, model: str) -> None:
    """Set the model preference for a specific user"""
    # Create session if it doesn't exist
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "messages": [],
            "model": None,
            "last_activity": time.time()
        }
    
    # Set model preference
    user_sessions[user_id]["model"] = model
    
    # Update last activity timestamp
    user_sessions[user_id]["last_activity"] = time.time()

def cleanup_sessions() -> None:
    """Remove inactive sessions to free up memory"""
    current_time = time.time()
    inactive_users = []
    
    # Find inactive sessions
    for user_id, session in user_sessions.items():
        if current_time - session["last_activity"] > SESSION_TIMEOUT:
            inactive_users.append(user_id)
    
    # Remove inactive sessions
    for user_id in inactive_users:
        del user_sessions[user_id]
    
    return len(inactive_users)