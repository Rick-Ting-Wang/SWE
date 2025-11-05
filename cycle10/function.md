# Komodo Hub - Functional Blocks Documentation

## System Architecture Overview

Komodo Hub is a conservation education platform built with a modular architecture that supports 10 different user roles. The system follows a layered architecture including configuration layer, data layer, service layer, routing layer, and presentation layer.

## Core Functional Modules

### 1. User Authentication & Authorization Module

#### Function Description
- User registration and login
- Password encryption and verification
- Session management
- Role-based access control

#### Related Files
- `services/__init__.py` - `AuthService`
- `models/user_models.py` - `UserModel`
- `routes/__init__.py` - Login/Registration routes

#### Main Methods
- `authenticate_user(email, password)` - User authentication
- `register_user(username, email, password, user_type)` - User registration
- `hash_password(password)` - Password encryption

### 2. User Management Module

#### Function Description
- User information management
- User profile maintenance
- Messaging system
- Avatar management

#### Related Files
- `services/__init__.py` - `UserService`
- `models/user_models.py` - `UserModel`, `MessageModel`
- `routes/__init__.py` - User center routes

#### Main Methods
- `get_user_profile(user_id)` - Get user profile
- `get_received_messages(user_id)` - Get received messages
- `send_message(sender_id, recipient_id, message_text)` - Send message

### 3. Organization Management Module

#### Function Description
- Organization creation and management
- Organization member management
- Permission control
- Access code management

#### Related Files
- `services/__init__.py` - `OrganizationService`
- `models/user_models.py` - `OrganizationModel`
- `routes/__init__.py` - Organization related routes

#### Main Methods
- `create_organization(org_type, org_name, org_profile, is_public, creator_id)` - Create organization
- `join_organization(org_id, user_id, access_code)` - Join organization
- `get_user_organizations(user_id)` - Get user organizations

### 4. Education Management Module

#### Function Description
- Course creation and management
- Course enrollment
- Program creation and management
- Program enrollment
- Activity creation
- Assignment submission and grading

#### Related Files
- `services/__init__.py` - `EducationService`
- `models/education_models.py` - `ClassModel`, `ProgramModel`, `ActivityModel`, `SubmissionModel`
- `routes/__init__.py` - Education related routes

#### Main Methods
- `create_class(org_id, teacher_id, class_name, syllabus)` - Create course
- `enroll_in_class(class_id, student_id)` - Enroll in course
- `create_program(program_name, description, program_type)` - Create program
- `enroll_in_program(program_id, user_id, org_id)` - Enroll in program
- `create_activity(program_id, class_id, activity_name, activity_type, description, created_by)` - Create activity
- `submit_assignment(activity_id, student_id, submission_data, submission_file_path)` - Submit assignment
- `grade_submission(submission_id, teacher_id, grade, feedback)` - Grade assignment

### 5. Content Management Module

#### Function Description
- Content upload and management
- Species sighting reports
- Creative canvas saving
- Business analytics recording

#### Related Files
- `services/__init__.py` - `ContentService`
- `models/content_models.py` - `ContentModel`, `SightingModel`, `AnalyticsModel`, `CanvasModel`
- `routes/__init__.py` - Content related routes

#### Main Methods
- `upload_content(title, content_type, content_data, created_by, org_id, is_public)` - Upload content
- `report_sighting(species_name, location, date_time, description, photo_path, reported_by)` - Report sighting
- `record_analytics(metric_type, metric_value, metric_data)` - Record analytics
- `save_canvas(user_id, program_id, assets)` - Save canvas

### 6. Database Management Layer

#### Function Description
- Database connection management
- Connection pool management
- Query execution
- Error handling

#### Related Files
- `models/__init__.py` - `DatabaseManager`, `BaseModel`

#### Main Methods
- `execute_query(query, params)` - Execute query
- `execute_update(query, params)` - Execute update
- `execute_insert(query, params)` - Execute insert
- `cursor()` - Database cursor context manager

### 7. Configuration Management Module

#### Function Description
- Application configuration management
- Environment variable handling
- Different environment configurations

#### Related Files
- `config/__init__.py` - `Config`, `DevelopmentConfig`, `ProductionConfig`, `TestingConfig`

#### Main Configuration Items
- Database connection configuration
- Session configuration
- File upload configuration
- Application settings

### 8. Utility Functions Module

#### Function Description
- Common utility functions
- Access log recording
- Permission checking
- Data type definitions

#### Related Files
- `utils/__init__.py`

#### Main Methods
- `log_access(db_manager, user_id, action, target_type, target_id)` - Record access log
- `require_role(db_manager, user_id, allowed_roles)` - Check role permissions
- `get_user_types()` - Get user type list
- `get_program_types()` - Get program type list

### 9. Route Management Layer

#### Function Description
- Route registration and management
- Request handling
- Session management
- Error handling

#### Related Files
- `routes/__init__.py` - `RouteManager`

#### Main Routes
- Authentication routes: `/`, `/register`, `/logout`
- User routes: `/user_center`
- Organization routes: `/create_organization`, `/join_organization`
- Education routes: `/create_class`, `/enroll_class`, `/create_program`, `/enroll_program`, `/create_activity`, `/submit_assignment`, `/grade_submission`
- Content routes: `/upload_content`, `/report_sighting`, `/save_canvas`, `/record_analytics`
- Message routes: `/send_message`

### 10. Frontend Presentation Layer

#### Function Description
- HTML template rendering
- Static resource management
- User interface interaction
- Responsive design

#### Related Files
- `templates/` - All HTML templates
- `static/css/style.css` - Stylesheet
- `static/js/main.js` - JavaScript

#### Main Templates
- `base.html` - Base template
- `main_menu.html` - Main menu
- `login.html` - Login page
- `register.html` - Registration page
- `user_center.html` - User center
- Various functional page templates

## Data Model Relationships

### User Related Tables
- `users` - Basic user information
- `user_profiles` - User detailed profiles
- `access_logs` - Access logs

### Organization Related Tables
- `organizations` - Organization information
- `organization_members` - Organization members

### Education Related Tables
- `classes` - Course information
- `class_enrollments` - Course enrollments
- `programs` - Program information
- `program_enrollments` - Program enrollments
- `activities` - Activity information
- `submissions` - Assignment submissions
- `assessments` - Assignment grading

### Content Related Tables
- `content_library` - Content library
- `species_sightings` - Species sightings
- `business_analytics` - Business analytics
- `creative_canvas` - Creative canvas
- `messages` - Messaging system

## Permission Control Matrix

| User Role | Create Organization | Create Course | Create Program | Create Activity | Grade Assignment | Record Analytics |
|-----------|-------------------|---------------|----------------|-----------------|------------------|------------------|
| admin     | ✅                | ✅            | ✅             | ✅              | ✅               | ✅               |
| principal | ✅                | ❌            | ✅             | ❌              | ❌               | ❌               |
| school_admin | ✅             | ✅            | ❌             | ❌              | ✅               | ❌               |
| teacher   | ❌                | ✅            | ❌             | ✅              | ✅               | ❌               |
| student   | ❌                | ❌            | ❌             | ❌              | ❌               | ❌               |
| community_chair | ✅          | ❌            | ✅             | ❌              | ❌               | ❌               |
| community_member | ❌         | ❌            | ❌             | ❌              | ❌               | ❌               |
| public    | ❌                | ❌            | ❌             | ❌              | ❌               | ❌               |

## Extensibility Notes

The current architecture design has good extensibility:

1. **New Functional Modules**: Can add new models, services, and routes in corresponding layers
2. **New User Roles**: Can add new roles in the permission control matrix
3. **New Data Types**: Can add new tables and fields in data models
4. **API Extensions**: Can add REST API layer to support mobile applications
5. **Third-party Integrations**: Can add third-party service integrations in the service layer

## Testing Infrastructure

The system includes comprehensive testing capabilities:
- Unit tests for all models and services
- Integration tests for database operations
- Mock testing for external dependencies
- Configuration testing for different environments

## Security Features

- Password encryption using SHA-256
- Session-based authentication
- Role-based access control
- SQL injection prevention through parameterized queries
- Access logging for security auditing
- File upload validation and size limits
- Student privacy protection (profiles private by default)