"""Database manager for PostgreSQL interactions."""

import asyncpg
from typing import Optional

class DatabaseManager:
    """Manages database connections and queries."""
    
    def __init__(self, config: dict):
        """
        Initialize database manager with configuration.
        
        Args:
            config: Database connection configuration dictionary
        """
        self.config = config
        self.connection = None
    
    async def connect(self):
        """Establish database connection."""
        try:
            self.connection = await asyncpg.connect(**self.config)
            print("Connected to database successfully")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise
    
    async def execute_query(self, query: str) -> Optional[int]:
        """
        Execute SQL query and return first result.
        
        Args:
            query: SQL query to execute
            
        Returns:
            First column of first row as integer, or None on error
        """
        try:
            result = await self.connection.fetchrow(query)
            return int(result[0]) if result else None
        except Exception as e:
            print(f"Database query error: {e}")
            return None
    
    async def close(self):
        """Close database connection."""
        if self.connection:
            await self.connection.close()
            print("Database connection closed")