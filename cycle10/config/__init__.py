"""
Configuration module for Komodo Hub Flask application
"""
import os
from typing import Dict, Any


class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

    # Database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', '3306'))
    DB_NAME = os.environ.get('DB_NAME', 'komodo')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mysql')

    # Session configuration
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')

    # Application settings
    APP_NAME = "Komodo Hub"
    APP_VERSION = "1.0.0"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DB_HOST = os.environ.get('DB_HOST', 'localhost')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DB_HOST = os.environ.get('DB_HOST', 'localhost')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DB_NAME = os.environ.get('TEST_DB_NAME', 'komodo_test')


config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}