"""
Test Utilities and Helpers for Komodo Hub

This module contains utility functions and helpers for testing the Komodo Hub platform.
Provides mock data creation, test assertions, and testing utilities.
"""

import os
import sys
import tempfile
import shutil
import json
import hashlib
from datetime import datetime, timedelta
from unittest.mock import Mock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test database configuration
TEST_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'test_user',
    'password': 'test_password',
    'database': 'test_komodo_db',
    'charset': 'utf8mb4'
}

# Mock user types for testing
MOCK_USER_TYPES = [
    'admin', 'project_director', 'principal', 'school_admin',
    'teacher', 'student', 'community_chair', 'community_member',
    'security_officer', 'public'
]

# Mock organization types
MOCK_ORG_TYPES = ['school', 'community', 'conservation', 'research']

# Mock program types
MOCK_PROGRAM_TYPES = ['conservation', 'education', 'research', 'regional']

# Mock activity types
MOCK_ACTIVITY_TYPES = ['assignment', 'quiz', 'project', 'field_work', 'presentation']

# Mock content types
MOCK_CONTENT_TYPES = ['article', 'report', 'photo', 'video', 'educational']


def create_mock_db_manager():
    """Create a mock database manager for testing"""
    mock_db = Mock()

    # Configure common mock behaviors
    mock_db.execute_query.return_value = []
    mock_db.execute_insert.return_value = 1
    mock_db.execute_update.return_value = 1
    mock_db.execute_delete.return_value = 1

    return mock_db


def create_test_user_data(user_id=1, username="testuser", user_type="student"):
    """Create standardized test user data"""
    return {
        'user_id': user_id,
        'username': username,
        'email': f"{username}@example.com",
        'password': 'hashed_password_123',
        'user_type': user_type,
        'is_active': 1,
        'created_at': '2024-01-01 10:00:00',
        'last_login': '2024-01-01 10:00:00'
    }


def create_test_org_data(org_id=1, org_type="school", is_public=True):
    """Create standardized test organization data"""
    return {
        'org_id': org_id,
        'org_type': org_type,
        'org_name': f"Test {org_type.title()} {org_id}",
        'org_profile': f"Test {org_type} organization",
        'is_public': is_public,
        'access_code': 'ABC123' if not is_public else None,
        'created_at': '2024-01-01 10:00:00'
    }


def create_test_program_data(program_id=1, program_type="conservation"):
    """Create standardized test program data"""
    return {
        'program_id': program_id,
        'program_name': f"Test {program_type.title()} Program {program_id}",
        'description': f"Test {program_type} program description",
        'program_type': program_type,
        'created_at': '2024-01-01 10:00:00'
    }


def create_test_class_data(class_id=1, org_id=1, teacher_id=1):
    """Create standardized test class data"""
    return {
        'class_id': class_id,
        'org_id': org_id,
        'teacher_id': teacher_id,
        'class_name': f"Test Class {class_id}",
        'syllabus': f"Test syllabus for class {class_id}",
        'max_students': 30,
        'created_at': '2024-01-01 10:00:00'
    }


def create_test_activity_data(activity_id=1, program_id=1, class_id=1):
    """Create standardized test activity data"""
    return {
        'activity_id': activity_id,
        'program_id': program_id,
        'class_id': class_id,
        'activity_name': f"Test Activity {activity_id}",
        'activity_type': 'assignment',
        'description': f"Test description for activity {activity_id}",
        'due_date': '2024-02-01 23:59:59',
        'created_by': 1,
        'created_at': '2024-01-01 10:00:00'
    }


def create_test_content_data(content_id=1, content_type="article"):
    """Create standardized test content data"""
    return {
        'content_id': content_id,
        'title': f"Test {content_type.title()} {content_id}",
        'content_type': content_type,
        'content_data': f"Test content data for {content_type} {content_id}",
        'created_by': 1,
        'org_id': 1,
        'is_public': True,
        'created_at': '2024-01-01 10:00:00'
    }


def create_test_sighting_data(sighting_id=1):
    """Create standardized test sighting data"""
    return {
        'sighting_id': sighting_id,
        'species_name': 'Komodo Dragon',
        'location': 'Komodo National Park',
        'date_time': '2024-01-01 14:30:00',
        'description': 'Spotted adult komodo dragon near water source',
        'photo_path': f'/uploads/komodo{sighting_id}.jpg',
        'reported_by': 1,
        'reported_at': '2024-01-01 14:35:00'
    }


def create_temp_directory():
    """Create a temporary directory for test files"""
    return tempfile.mkdtemp(prefix='komodo_test_')


def cleanup_temp_directory(temp_dir):
    """Clean up temporary directory"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


class TestConfig:
    """Test configuration class"""

    def __init__(self):
        self.SECRET_KEY = 'test-secret-key-12345'
        self.DB_HOST = TEST_DB_CONFIG['host']
        self.DB_PORT = TEST_DB_CONFIG['port']
        self.DB_NAME = TEST_DB_CONFIG['database']
        self.DB_USER = TEST_DB_CONFIG['user']
        self.DB_PASSWORD = TEST_DB_CONFIG['password']
        self.MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
        self.UPLOAD_FOLDER = '/tmp/test_uploads'
        self.AVATAR_UPLOAD_FOLDER = '/tmp/test_avatars'
        self.SESSION_PERMANENT = False


def setup_test_environment():
    """Set up the test environment"""
    # Create test upload directories
    os.makedirs('/tmp/test_uploads', exist_ok=True)
    os.makedirs('/tmp/test_avatars', exist_ok=True)

    # Set environment variables for testing
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['FLASK_DEBUG'] = '0'

    return TestConfig()


def teardown_test_environment():
    """Clean up the test environment"""
    # Clean up test directories
    if os.path.exists('/tmp/test_uploads'):
        shutil.rmtree('/tmp/test_uploads')
    if os.path.exists('/tmp/test_avatars'):
        shutil.rmtree('/tmp/test_avatars')

    # Clean up environment variables
    if 'FLASK_ENV' in os.environ:
        del os.environ['FLASK_ENV']
    if 'FLASK_DEBUG' in os.environ:
        del os.environ['FLASK_DEBUG']


# Test assertions helpers
def assert_user_data_equal(self, expected, actual):
    """Helper to assert user data equality"""
    self.assertEqual(expected['user_id'], actual['user_id'])
    self.assertEqual(expected['username'], actual['username'])
    self.assertEqual(expected['email'], actual['email'])
    self.assertEqual(expected['user_type'], actual['user_type'])
    self.assertEqual(expected['is_active'], actual['is_active'])


def assert_org_data_equal(self, expected, actual):
    """Helper to assert organization data equality"""
    self.assertEqual(expected['org_id'], actual['org_id'])
    self.assertEqual(expected['org_type'], actual['org_type'])
    self.assertEqual(expected['org_name'], actual['org_name'])
    self.assertEqual(expected['is_public'], actual['is_public'])


def assert_success_response(self, response):
    """Helper to assert successful API response"""
    self.assertIsInstance(response, dict)
    self.assertIn('success', response)
    self.assertTrue(response['success'])


def assert_error_response(self, response, expected_error=None):
    """Helper to assert error API response"""
    self.assertIsInstance(response, dict)
    self.assertIn('success', response)
    self.assertFalse(response['success'])
    self.assertIn('error', response)
    if expected_error:
        self.assertIn(expected_error, response['error'])


def hash_password(password):
    """Utility function to hash passwords (same as in AuthService)"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_mock_session(user_id=1, username="testuser", user_type="student"):
    """Create a mock session object"""
    return {
        'user_id': user_id,
        'username': username,
        'user_type': user_type,
        'logged_in': True
    }


def create_mock_request(method="GET", form_data=None, args=None, files=None):
    """Create a mock request object"""
    mock_request = Mock()
    mock_request.method = method
    mock_request.form = form_data or {}
    mock_request.args = args or {}
    mock_request.files = files or {}
    return mock_request


if __name__ == '__main__':
    # Test the configuration
    print("Test Configuration Loaded")
    print(f"Test DB Config: {TEST_DB_CONFIG}")
    print(f"User Types: {MOCK_USER_TYPES}")
    print(f"Org Types: {MOCK_ORG_TYPES}")

    # Test data creation
    test_user = create_test_user_data()
    test_org = create_test_org_data()
    print(f"Sample Test User: {test_user}")
    print(f"Sample Test Org: {test_org}")

    # Test mock creation
    mock_db = create_mock_db_manager()
    print("Mock DB Manager created successfully")