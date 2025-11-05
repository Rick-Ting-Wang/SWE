"""
Komodo Hub - Database Configuration File
Database configuration for Komodo Hub system
"""

import os
from typing import Optional


class DatabaseConfig:
    """Database configuration class"""

    def __init__(self):
        # Database connection parameters
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.database = os.getenv('DB_NAME', 'komodo')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'mysql')
        self.charset = 'utf8mb4'

        # Connection pool configuration
        self.pool_size = 5
        self.max_overflow = 10
        self.pool_timeout = 30

    def get_connection_string(self) -> str:
        """Get database connection string"""
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"

    def get_connection_params(self) -> dict:
        """Get database connection parameters"""
        return {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'charset': self.charset
        }


# Global configuration instance
db_config = DatabaseConfig()
