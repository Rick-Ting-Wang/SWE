-- ###########################################################
-- Script Purpose: Create full business table structure for users, organizations, classes, activities, etc.
-- Applicable Database: MySQL 8.0+ (supports ENUM, CHECK constraints, JSON type)
-- Instructions:
-- 1. Replace `your_database_name` with your actual database name.
-- 2. Make sure the current user has CREATE TABLE permission before execution.
-- 3. Table creation order is sorted by foreign key dependencies, do NOT adjust randomly.
-- 4. To recreate tables, you can add `DROP TABLE IF EXISTS table_name;` before each CREATE TABLE (use with caution, this will delete data).
-- ###########################################################

-- Switch to target database (the database must be created before executing this script)
USE your_database_name;

-- 1. Users Table (Stores all user roles)
CREATE TABLE users
(
    user_id       INT PRIMARY KEY AUTO_INCREMENT,
    username      VARCHAR(50) UNIQUE  NOT NULL,
    email         VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255)        NOT NULL,
    user_type     ENUM('admin', 'principal', 'school_admin', 'teacher', 
        'student', 'community_chair', 'community_member', 'public') NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login    TIMESTAMP NULL,
    INDEX         idx_user_type (user_type),
    INDEX         idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: users table created


-- 2. Organizations Table (Schools/communities and similar organizations)
CREATE TABLE organizations
(
    org_id              INT PRIMARY KEY AUTO_INCREMENT,
    org_type            ENUM('school', 'community') NOT NULL,
    org_name            VARCHAR(200) NOT NULL,
    org_profile         TEXT,
    is_public           BOOLEAN   DEFAULT TRUE,
    subscription_status ENUM('active', 'inactive', 'pending') DEFAULT 'pending',
    subscription_date   DATE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX               idx_org_type (org_type),
    INDEX               idx_subscription_status (subscription_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: organizations table created


-- 3. Organization Members Table (User-organization relation, many-to-many)
CREATE TABLE organization_members
(
    membership_id INT PRIMARY KEY AUTO_INCREMENT,
    org_id        INT  NOT NULL,
    user_id       INT  NOT NULL,
    role          ENUM('principal', 'admin', 'teacher', 'student', 'chairman', 'member') NOT NULL,
    access_code   VARCHAR(50) UNIQUE,
    joined_date   DATE NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations (org_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_org_user (org_id, user_id), -- A user has only one identity in the same organization
    INDEX         idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: organization_members table created


-- 4. Classes Table (Courses under a school organization)
CREATE TABLE classes
(
    class_id   INT PRIMARY KEY AUTO_INCREMENT,
    org_id     INT          NOT NULL,
    teacher_id INT          NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    syllabus   TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations (org_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users (user_id) ON DELETE CASCADE,
    INDEX      idx_teacher (teacher_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: classes table created


-- 5. Class Enrollments Table (Student-class relation)
CREATE TABLE class_enrollments
(
    enrollment_id   INT PRIMARY KEY AUTO_INCREMENT,
    class_id        INT  NOT NULL,
    student_id      INT  NOT NULL,
    enrollment_date DATE NOT NULL,
    status          ENUM('active', 'inactive') DEFAULT 'active',
    FOREIGN KEY (class_id) REFERENCES classes (class_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users (user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_class_student (class_id, student_id), -- A student can only enroll in the same class once
    INDEX           idx_student (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: class_enrollments table created


-- 6. Programs Table (General programs/activities)
CREATE TABLE programs
(
    program_id   INT PRIMARY KEY AUTO_INCREMENT,
    program_name VARCHAR(200) NOT NULL,
    description  TEXT,
    program_type ENUM('internal', 'local', 'regional', 'national') NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX        idx_program_type (program_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: programs table created


-- 7. Program Enrollments Table (Relation between users/organizations and programs, supports individual or organization)
CREATE TABLE program_enrollments
(
    enrollment_id   INT PRIMARY KEY AUTO_INCREMENT,
    program_id      INT  NOT NULL,
    user_id         INT, -- Individual enrollment (can be NULL)
    org_id          INT, -- Organization enrollment (can be NULL)
    enrollment_date DATE NOT NULL,
    status          ENUM('active', 'completed', 'dropped') DEFAULT 'active',
    FOREIGN KEY (program_id) REFERENCES programs (program_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES organizations (org_id) ON DELETE CASCADE,
    CHECK (user_id IS NOT NULL OR org_id IS NOT NULL), -- Ensure at least one is not NULL
    INDEX           idx_program (program_id),
    INDEX           idx_user (user_id),
    INDEX           idx_org (org_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: program_enrollments table created


-- 8. Activities Table (Concrete activities under a program/class)
CREATE TABLE activities
(
    activity_id   INT PRIMARY KEY AUTO_INCREMENT,
    program_id    INT          NOT NULL,
    class_id      INT, -- Optional related class (can be NULL)
    activity_name VARCHAR(200) NOT NULL,
    activity_type ENUM('in-class', 'outdoor', 'challenge', 'game', 'assessment') NOT NULL,
    description   TEXT,
    created_by    INT          NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs (program_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes (class_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE CASCADE,
    INDEX         idx_program (program_id),
    INDEX         idx_class (class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: activities table created


-- 9. Content Library Table (Articles/photos/educational materials etc.)
CREATE TABLE content_library
(
    content_id   INT PRIMARY KEY AUTO_INCREMENT,
    title        VARCHAR(300) NOT NULL,
    content_type ENUM('article', 'essay', 'report', 'sighting', 'photo', 
          'video', 'educational_material') NOT NULL,
    content_data TEXT,
    created_by   INT          NOT NULL,
    org_id       INT, -- Optional related organization (can be NULL)
    is_public    BOOLEAN   DEFAULT FALSE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES organizations (org_id) ON DELETE CASCADE,
    INDEX        idx_content_type (content_type),
    INDEX        idx_org (org_id),
    INDEX        idx_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: content_library table created


-- 10. Species Sightings Table (Records of species sightings)
CREATE TABLE species_sightings
(
    sighting_id  INT PRIMARY KEY AUTO_INCREMENT,
    species_name VARCHAR(100) NOT NULL,
    location     VARCHAR(200) NOT NULL,
    date_time    DATETIME     NOT NULL,
    description  TEXT,
    photo_path   VARCHAR(500),
    reported_by  INT          NOT NULL,
    verified     BOOLEAN   DEFAULT FALSE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reported_by) REFERENCES users (user_id) ON DELETE CASCADE,
    INDEX        idx_species (species_name),
    INDEX        idx_reporter (reported_by),
    INDEX        idx_verified (verified)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: species_sightings table created


-- 11. Submissions Table (Student submissions for activities/assignments)
CREATE TABLE submissions
(
    submission_id        INT PRIMARY KEY AUTO_INCREMENT,
    activity_id          INT NOT NULL,
    student_id           INT NOT NULL,
    submission_data      TEXT,
    submission_file_path VARCHAR(500),
    submission_date      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status               ENUM('submitted', 'graded', 'returned') DEFAULT 'submitted',
    FOREIGN KEY (activity_id) REFERENCES activities (activity_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users (user_id) ON DELETE CASCADE,
    INDEX                idx_activity (activity_id),
    INDEX                idx_student (student_id),
    INDEX                idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: submissions table created


-- 12. Assessments Table (Teacher grading/feedback on submissions)
CREATE TABLE assessments
(
    assessment_id INT PRIMARY KEY AUTO_INCREMENT,
    submission_id INT NOT NULL,
    teacher_id    INT NOT NULL,
    grade         VARCHAR(10), -- Supports letter/number grades (e.g. A, 90)
    feedback      TEXT,
    assessed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (submission_id) REFERENCES submissions (submission_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users (user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_submission (submission_id), -- Only one assessment per submission
    INDEX         idx_teacher (teacher_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: assessments table created


-- 13. Messages Table (User-to-user private messages)
CREATE TABLE messages
(
    message_id   INT PRIMARY KEY AUTO_INCREMENT,
    sender_id    INT  NOT NULL,
    recipient_id INT  NOT NULL,
    message_text TEXT NOT NULL,
    sent_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at      TIMESTAMP NULL, -- Read time (NULL = unread)
    FOREIGN KEY (sender_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users (user_id) ON DELETE CASCADE,
    INDEX        idx_sender (sender_id),
    INDEX        idx_recipient (recipient_id),
    INDEX        idx_read (read_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: messages table created


-- 14. Notes Table (Teacher notes on submissions/content/sightings)
CREATE TABLE notes
(
    note_id     INT PRIMARY KEY AUTO_INCREMENT,
    teacher_id  INT  NOT NULL,
    target_type ENUM('submission', 'content', 'sighting') NOT NULL,
    target_id   INT  NOT NULL, -- ID of the related object (such as submission_id, content_id)
    note_text   TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users (user_id) ON DELETE CASCADE,
    INDEX       idx_teacher (teacher_id),
    INDEX       idx_target (target_type, target_id) -- Combined index for quick note lookup
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: notes table created


-- 15. User Profiles Table (User profile extension, one-to-one with users)
CREATE TABLE user_profiles
(
    profile_id   INT PRIMARY KEY AUTO_INCREMENT,
    user_id      INT NOT NULL,
    avatar_path  VARCHAR(500), -- Avatar file path
    color_scheme VARCHAR(50), -- UI color scheme (e.g. "light", "dark")
    bio          TEXT, -- User bio
    is_public    BOOLEAN DEFAULT TRUE, -- Is the profile public
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user (user_id), -- Only one profile per user
    INDEX        idx_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: user_profiles table created


-- 16. Creative Canvas Table (User creative assets in a program)
CREATE TABLE creative_canvas
(
    canvas_id  INT PRIMARY KEY AUTO_INCREMENT,
    user_id    INT NOT NULL,
    program_id INT NOT NULL,
    assets     JSON, -- Stores creative assets (e.g. JSON configuration of elements)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES programs (program_id) ON DELETE CASCADE,
    INDEX      idx_user (user_id),
    INDEX      idx_program (program_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: creative_canvas table created


-- 17. Access Logs Table (User operation logs, for audit/tracing)
CREATE TABLE access_logs
(
    log_id      BIGINT PRIMARY KEY AUTO_INCREMENT, -- Use BIGINT to avoid overflow due to large number of logs
    user_id     INT, -- NULL for anonymous operations
    action      VARCHAR(200) NOT NULL, -- Operation description (e.g. "login", "create_content")
    target_type VARCHAR(50), -- Target object type (e.g. "user", "activity")
    target_id   INT, -- Target object ID
    timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address  VARCHAR(45), -- Supports IPv4 (15 chars) and IPv6 (39 chars)
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE SET NULL, -- Keep logs after user deletion, set user_id to NULL
    INDEX       idx_user (user_id),
    INDEX       idx_timestamp (timestamp), -- Query logs by time range
    INDEX       idx_action (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: access_logs table created


-- 18. Business Analytics Table (Stores statistical metric data)
CREATE TABLE business_analytics
(
    analytics_id INT PRIMARY KEY AUTO_INCREMENT,
    metric_type  VARCHAR(100) NOT NULL, -- Metric type (e.g. "daily_active_users", "program_enrollments")
    metric_value DECIMAL(15, 2), -- Metric value (supports decimals, e.g. conversion rate 23.5%)
    metric_data  JSON, -- Additional metric data (e.g. active users by role)
    recorded_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX        idx_metric_type (metric_type),
    INDEX        idx_recorded_at (recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Note: business_analytics table created


COMMIT;
SELECT 'All 18 tables created successfully!' AS result;
