"""
Komodo Hub - Conservation Education Platform
Enhanced Flask application with improved architecture
"""
import os
from flask import Flask
from dotenv import load_dotenv
from config import config
from routes import RouteManager


def create_app(config_name='default'):
    """
    Application factory function
    """
    # Load environment variables
    load_dotenv()

    # Create Flask app
    app = Flask(__name__)

    # Configure app
    app_config = config[config_name]
    app.config.from_object(app_config)

    # Ensure required directories exist
    ensure_directories(app)

    # Initialize route manager
    route_manager = RouteManager(app, app_config)
    route_manager.register_routes()

    return app


def ensure_directories(app):
    """Ensure required directories exist"""
    directories = [
        os.path.join(app.root_path, 'templates'),
        os.path.join(app.root_path, 'static'),
        os.path.join(app.root_path, 'static', 'css'),
        os.path.join(app.root_path, 'static', 'js'),
        os.path.join(app.root_path, 'static', 'images'),
        os.path.join(app.root_path, 'static', 'avatar'),
        os.path.join(app.root_path, 'uploads')
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


if __name__ == '__main__':
    # Create and run application
    app = create_app('development')

    print("=" * 50)
    print("Komodo Hub - Conservation Education Platform")
    print("Enhanced Architecture Version")
    print("=" * 50)
    print("Starting server...")
    print(f"Debug mode: {app.config['DEBUG']}")
    print(f"Database: {app.config['DB_NAME']}@{app.config['DB_HOST']}")
    print("=" * 50)

    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5001
    )
