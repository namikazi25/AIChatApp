import json
import sqlite3
from typing import Dict, List, Any, Optional
from backend.storage import StorageBackend

class SQLiteStorage(StorageBackend):
    """SQLite implementation of the storage backend"""
    
    def __init__(self, db_path: str = "sessions.db"):
        """Initialize the SQLite storage backend
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_key TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            last_activity REAL NOT NULL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a session by key
        
        Args:
            key: The session key
            
        Returns:
            The session data or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM sessions WHERE session_key = ?", (key,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            # Parse JSON data
            return json.loads(result[0])
        
        return None
    
    def set(self, key: str, data: Dict[str, Any]) -> None:
        """Set or update a session
        
        Args:
            key: The session key
            data: The session data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert data to JSON
        json_data = json.dumps(data)
        
        # Extract last_activity from data
        last_activity = data.get("last_activity", 0)
        
        # Insert or replace session
        cursor.execute("""
        INSERT OR REPLACE INTO sessions (session_key, data, last_activity)
        VALUES (?, ?, ?)
        """, (key, json_data, last_activity))
        
        conn.commit()
        conn.close()
    
    def delete(self, key: str) -> None:
        """Delete a session
        
        Args:
            key: The session key
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE session_key = ?", (key,))
        
        conn.commit()
        conn.close()
    
    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """Get all sessions
        
        Returns:
            A dictionary of all sessions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT session_key, data FROM sessions")
        results = cursor.fetchall()
        
        conn.close()
        
        sessions = {}
        for key, data in results:
            sessions[key] = json.loads(data)
        
        return sessions