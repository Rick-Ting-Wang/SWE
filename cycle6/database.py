"""
Komodo Hub - Database Connection Manager
Database connection manager with connection pooling
"""

import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from typing import Optional, Dict, Any, List, Tuple
import logging
from config import db_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database connection manager"""

    def __init__(self):
        self.config = db_config.get_connection_params()
        self.connection = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = pymysql.connect(
                **self.config,
                cursorclass=DictCursor,
                autocommit=False
            )
            logger.info("Database connection successful")
            return self.connection
        except pymysql.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    @contextmanager
    def get_cursor(self):
        """Get database cursor (context manager)"""
        if not self.connection or not self.connection.open:
            self.connect()

        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            cursor.close()

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Execute query and return results"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        """Execute update/insert/delete operation"""
        with self.get_cursor() as cursor:
            affected_rows = cursor.execute(query, params or ())
            return affected_rows

    def execute_insert(self, query: str, params: Optional[Tuple] = None) -> int:
        """Execute insert operation and return inserted ID"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid

    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        """Execute batch operations"""
        with self.get_cursor() as cursor:
            affected_rows = cursor.executemany(query, params_list)
            return affected_rows


# Global database manager instance
db = DatabaseManager()


class BaseModel:
    """Base model class, provides common database operation methods"""

    table_name = None
    primary_key = 'id'

    @classmethod
    def find_by_id(cls, id_value: int) -> Optional[Dict[str, Any]]:
        """Find record by ID"""
        query = f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = %s"
        results = db.execute_query(query, (id_value,))
        return results[0] if results else None

    @classmethod
    def find_all(cls, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Find all records (with pagination)"""
        query = f"SELECT * FROM {cls.table_name} LIMIT %s OFFSET %s"
        return db.execute_query(query, (limit, offset))

    @classmethod
    def find_by_condition(cls, conditions: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """Find records by condition"""
        where_clauses = [f"{key} = %s" for key in conditions.keys()]
        where_sql = " AND ".join(where_clauses)
        query = f"SELECT * FROM {cls.table_name} WHERE {where_sql} LIMIT %s"
        params = tuple(conditions.values()) + (limit,)
        return db.execute_query(query, params)

    @classmethod
    def insert(cls, data: Dict[str, Any]) -> int:
        """Insert new record"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})"
        return db.execute_insert(query, tuple(data.values()))

    @classmethod
    def update(cls, id_value: int, data: Dict[str, Any]) -> int:
        """Update record"""
        set_clauses = [f"{key} = %s" for key in data.keys()]
        set_sql = ", ".join(set_clauses)
        query = f"UPDATE {cls.table_name} SET {set_sql} WHERE {cls.primary_key} = %s"
        params = tuple(data.values()) + (id_value,)
        return db.execute_update(query, params)

    @classmethod
    def delete(cls, id_value: int) -> int:
        """Delete record"""
        query = f"DELETE FROM {cls.table_name} WHERE {cls.primary_key} = %s"
        return db.execute_update(query, (id_value,))

    @classmethod
    def count(cls, conditions: Optional[Dict[str, Any]] = None) -> int:
        """Count records"""
        if conditions:
            where_clauses = [f"{key} = %s" for key in conditions.keys()]
            where_sql = " AND ".join(where_clauses)
            query = f"SELECT COUNT(*) as count FROM {cls.table_name} WHERE {where_sql}"
            params = tuple(conditions.values())
        else:
            query = f"SELECT COUNT(*) as count FROM {cls.table_name}"
            params = ()

        result = db.execute_query(query, params)
        return result[0]['count'] if result else 0
