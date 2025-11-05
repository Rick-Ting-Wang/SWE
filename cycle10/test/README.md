# Komodo Hub Testing Guide

This directory contains comprehensive unit tests for the Komodo Hub conservation education platform. The tests are organized by component type (services, models) and use mocking to isolate units from external dependencies.

## Test Structure

```
test/
├── README.md                    # This testing guide
├── test_services.py            # Unit tests for service layer
├── test_models.py              # Unit tests for data models
├── test_integration.py         # Integration tests (optional)
├── test_config.py              # Configuration and setup tests
└── test_data/                  # Test data fixtures (if needed)
```

## Prerequisites

Before running tests, ensure you have the required dependencies installed:

```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-mock

# Or install from requirements if available
pip install -r requirements-test.txt
```

## Running Tests

### Run All Tests

```bash
# From the project root directory
cd /Users/sukhoina/Team13-SWE-Groupwork/cycle10

# Run all tests with unittest
uv run python -m unittest discover test/

# Run all tests with pytest (alternative)
pytest test/

# Run with coverage report
pytest test/ --cov=. --cov-report=html
```

### Run Specific Test Files

```bash
# Run only service tests
uv run python -m unittest test.test_services

# Run only model tests
uv run python -m unittest test.test_models

# Run with pytest
pytest test/test_services.py
pytest test/test_models.py
```

### Run Specific Test Classes

```bash
# Run specific test class
uv run python -m unittest test.test_services.TestAuthService
uv run python -m unittest test.test_models.TestUserModel

# Run with pytest
pytest test/test_services.py::TestAuthService
pytest test/test_models.py::TestUserModel
```

### Run Specific Test Methods

```bash
# Run specific test method
uv run python -m unittest test.test_services.TestAuthService.test_hash_password
uv run python -m unittest test.test_models.TestUserModel.test_create_user_success

# Run with pytest
pytest test/test_services.py::TestAuthService::test_hash_password
pytest test/test_models.py::TestUserModel::test_create_user_success
```

## Test Categories

### 1. Service Tests (`test_services.py`)

Tests the business logic layer including:

- **AuthService**: User authentication, password hashing, role verification
- **UserService**: User profile management, messaging
- **OrganizationService**: Organization creation, membership management
- **EducationService**: Course/program creation, enrollment, grading
- **ContentService**: Content upload, species sightings, analytics

#### Key Test Scenarios:
- User registration with duplicate email handling
- Authentication with correct/incorrect passwords
- Organization access control (public vs private)
- Course enrollment capacity limits
- Assignment submission and grading workflow

### 2. Model Tests (`test_models.py`)

Tests the data access layer including:

- **DatabaseManager**: Connection management, query execution
- **UserModel**: User CRUD operations
- **OrganizationModel**: Organization and membership management
- **MessageModel**: Messaging system operations
- **Education Models**: Class, Program, Activity, Submission operations
- **Content Models**: Content, Sighting, Analytics, Canvas operations

#### Key Test Scenarios:
- Database connection pooling and error handling
- Transaction rollback on errors
- SQL injection prevention via parameterized queries
- Data validation and constraint handling
- Model relationship integrity

## Test Configuration

### Mock Database Setup

Tests use mocked database connections to avoid requiring a real database:

```python
from unittest.mock import Mock, patch

# Example of setting up mock database
self.mock_db_manager = Mock()
self.service = SomeService(self.mock_db_manager)

# Mock query results
self.mock_db_manager.execute_query.return_value = [
    {'id': 1, 'name': 'Test Item'}
]

# Mock insert operations
self.mock_db_manager.execute_insert.return_value = 123  # New ID
```

### Test Data Patterns

Common test data patterns used across tests:

```python
# User test data
mock_user = {
    'user_id': 1,
    'username': 'testuser',
    'email': 'test@example.com',
    'user_type': 'student',
    'is_active': 1
}

# Organization test data
mock_org = {
    'org_id': 1,
    'org_type': 'school',
    'org_name': 'Test School',
    'is_public': True,
    'access_code': None
}

# Content test data
mock_content = {
    'content_id': 1,
    'title': 'Test Article',
    'content_type': 'article',
    'created_by': 1,
    'is_public': True
}
```

## Writing New Tests

### Test Naming Conventions

- Test classes: `Test<ServiceName>` or `Test<ModelName>`
- Test methods: `test_<action>_<condition>_<expected_result>`
- Use descriptive names that explain what is being tested

### Example Test Structure

```python
import unittest
from unittest.mock import Mock
from services import AuthService

class TestAuthService(unittest.TestCase):
    """Test cases for AuthService"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_db_manager = Mock()
        self.auth_service = AuthService(self.mock_db_manager)

    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        # Arrange
        mock_user = {
            'user_id': 1,
            'email': 'test@example.com',
            'password': 'hashed_password',
            'is_active': 1
        }
        self.mock_db_manager.execute_query.return_value = [mock_user]

        # Act
        result = self.auth_service.authenticate_user('test@example.com', 'password')

        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['user']['user_id'], 1)

    def test_authenticate_user_wrong_password(self):
        """Test authentication failure with wrong password"""
        # Arrange
        mock_user = {
            'user_id': 1,
            'email': 'test@example.com',
            'password': 'different_hash',
            'is_active': 1
        }
        self.mock_db_manager.execute_query.return_value = [mock_user]

        # Act
        result = self.auth_service.authenticate_user('test@example.com', 'wrong_password')

        # Assert
        self.assertFalse(result['success'])
        self.assertIn('error', result)
```

### Best Practices

1. **Use Mocks Appropriately**: Mock external dependencies (database, file system, network)
2. **Test One Thing**: Each test should verify a single behavior or outcome
3. **Descriptive Names**: Test names should clearly indicate what's being tested
4. **Arrange-Act-Assert**: Structure tests with clear setup, action, and verification phases
5. **Edge Cases**: Test boundary conditions, error cases, and invalid inputs
6. **Independence**: Tests should not depend on each other or external state

## Coverage Goals

Aim for the following test coverage levels:

- **Line Coverage**: > 80%
- **Branch Coverage**: > 75%
- **Function Coverage**: 100% for public methods
- **Critical Paths**: 100% coverage for authentication, authorization, and data validation

### Generate Coverage Report

```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run -m unittest discover test/

# Generate coverage report
coverage report
coverage html  # Creates htmlcov/index.html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Continuous Integration

For CI/CD pipelines, add test execution to your workflow:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: |
        pytest test/ --cov=. --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure proper Python path setup
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```

2. **Mock Not Working**: Verify mock setup and return values
   ```python
   # Check mock was called
   self.mock_db_manager.execute_query.assert_called_once()

   # Check call arguments
   call_args = self.mock_db_manager.execute_query.call_args[0]
   self.assertIn('SELECT * FROM users', call_args[0])
   ```

3. **Database Connection Issues**: Tests should use mocks, not real connections

4. **Test Isolation**: Use `setUp()` and `tearDown()` methods to ensure clean state

### Debug Mode

Run tests in debug mode for detailed output:

```bash
# Verbose output
uv run python -m unittest discover test/ -v

# Debug specific test
uv run python -m unittest test.test_services.TestAuthService.test_authenticate_user_success -v
```

## Performance Testing

For performance-critical components:

```python
import time
import unittest

class TestPerformance(unittest.TestCase):
    """Performance tests for critical operations"""

    def test_user_authentication_performance(self):
        """Test authentication response time"""
        start_time = time.time()

        # Perform authentication
        result = self.auth_service.authenticate_user('test@example.com', 'password')

        end_time = time.time()
        response_time = end_time - start_time

        # Assert response time is acceptable (< 1 second)
        self.assertLess(response_time, 1.0)
        self.assertTrue(result['success'])
```

## Security Testing

Verify security measures are properly implemented:

```python
def test_sql_injection_prevention(self):
    """Test SQL injection prevention"""
    malicious_input = "'; DROP TABLE users; --"

    # This should not execute the malicious SQL
    result = self.user_model.get_user_by_email(malicious_input)

    # Verify parameterized query was used
    call_args = self.mock_db_manager.execute_query.call_args[0]
    self.assertEqual(call_args[1], (malicious_input,))
    self.assertNotIn(malicious_input, call_args[0])

def test_password_hashing(self):
    """Test password is properly hashed"""
    password = "test_password"

    # Password should be hashed, not stored in plain text
    self.user_model.create_user("user", "email@example.com", password, "student")

    call_args = self.mock_db_manager.execute_insert.call_args[0]
    stored_password = call_args[1][3]  # Password parameter

    # Verify password is hashed (SHA-256 produces 64 character hex string)
    self.assertEqual(len(stored_password), 64)
    self.assertNotEqual(stored_password, password)
```

## Test Maintenance

### Regular Updates

- Update tests when business logic changes
- Add tests for new features immediately
- Refactor tests to reduce duplication
- Remove obsolete tests for deprecated features

### Test Review

- Review test failures promptly
- Analyze coverage reports regularly
- Update test data to reflect current requirements
- Optimize slow-running tests

This testing guide ensures comprehensive coverage of the Komodo Hub platform while maintaining test quality and reliability. Regular execution of these tests helps catch regressions early and maintains code quality throughout development."}