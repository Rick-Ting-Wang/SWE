"""
Database models and connection management
"""
import pymysql
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from config import Config


class DatabaseManager:
    """Database connection manager with connection pooling"""

    def __init__(self, config: Config):
        self.config = config
        self._connection = None

    def get_connection(self):
        """Get database connection"""
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        return self._connection

    @contextmanager
    def cursor(self):
        """Context manager for database cursor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        with self.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an update query and return affected rows"""
        with self.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount

    def execute_insert(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an insert query and return last row ID"""
        with self.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid

    def close(self):
        """Close database connection"""
        if self._connection and self._connection.open:
            self._connection.close()
            self._connection = None


class BaseModel:
    """Base model class with common database operations"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def _execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute query with error handling"""
        try:
            return self.db.execute_query(query, params)
        except pymysql.Error as e:
            # Log error and re-raise
            print(f"Database error: {e}")
            raise

    def _execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute update with error handling"""
        try:
            return self.db.execute_update(query, params)
        except pymysql.Error as e:
            print(f"Database error: {e}")
            raise

    def _execute_insert(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute insert with error handling"""
        try:
            return self.db.execute_insert(query, params)
        except pymysql.Error as e:
            print(f"Database error: {e}")
            raise
