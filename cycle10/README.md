# Komodo Hub - Cycle 10

Enhanced Flask application with improved architecture for the Komodo Hub conservation education platform.

## Architecture Overview

This version features a clean, modular architecture with proper separation of concerns:

## Key Improvements

### 1. Modular Architecture
- **Configuration Management**: Environment-based configuration with different profiles
- **Data Layer**: Separated models for different domains (users, education, content)
- **Business Logic**: Service layer for business operations
- **Presentation Layer**: Clean route definitions with proper error handling

### 2. Better Code Organization
- **Separation of Concerns**: Each layer has clear responsibilities
- **Reusable Components**: Base classes and utilities for code reuse
- **Type Hints**: Improved code documentation and IDE support

### 3. Enhanced Frontend
- **Base Template**: Consistent layout across all pages
- **CSS Framework**: Modern, responsive design
- **JavaScript Enhancements**: Better user interactions
- **Template Inheritance**: DRY principle for templates

### 4. Improved Error Handling
- **Database Error Handling**: Proper exception handling for database operations
- **Form Validation**: Client-side and server-side validation
- **User Feedback**: Better flash message system

## Running the Application

### Prerequisites
- Python 3.8+
- MySQL database
- Required Python packages (see requirements.txt)

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables (optional):
   ```bash
   export DB_HOST=localhost
   export DB_PORT=3306
   export DB_NAME=komodo
   export DB_USER=root
   export DB_PASSWORD=mysql
   export SECRET_KEY=your-secret-key
   ```

3. Run the application:
   ```bash
   python app.py
   ```

### Database Setup
Make sure your MySQL database is running and the `komodo` database exists with the required tables. The database schema should match the one used in previous cycles.

## Features

- User authentication and registration
- Organization management (schools, communities)
- Course and program management
- Activity creation and assignment submission
- Content upload and species sighting reporting
- Messaging system
- User profiles and settings
- Analytics tracking

## Development Notes

This version maintains full compatibility with the existing database schema while providing a much cleaner and more maintainable codebase. The architecture is designed to be easily extensible for future features.

## Next Steps

- Add unit tests for services and models
- Implement API endpoints for mobile applications
- Add more sophisticated error handling
- Implement caching for better performance
- Add logging and monitoring
