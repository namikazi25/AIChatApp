from typing import Optional
import os
from dotenv import load_dotenv
from backend.storage import MemoryStorage, StorageBackend

# Load environment variables
load_dotenv()

# Default storage type
DEFAULT_STORAGE_TYPE = os.getenv("STORAGE_TYPE", "memory")

# Database configuration
DB_PATH = os.getenv("DB_PATH", "sessions.db")

def get_storage_backend() -> StorageBackend:
    """Get the configured storage backend based on environment variables
    
    Returns:
        The configured storage backend
    """
    storage_type = os.getenv("STORAGE_TYPE", DEFAULT_STORAGE_TYPE)
    
    if storage_type.lower() == "sqlite":
        # Import here to avoid circular imports
        from backend.db_storage import SQLiteStorage
        return SQLiteStorage(DB_PATH)
    else:
        # Default to memory storage
        return MemoryStorage()