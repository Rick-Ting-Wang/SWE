//fellows, please update the initial database script here
"""
数据库初始化脚本 - 创建表结构并插入初始数据
"""
import pymysql
import bcrypt
from datetime import datetime, date
import json

from config import Config

def get_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
def hash_password(password):
    """哈希密码"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_database():
    """创建数据库"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 删除旧数据库（如果存在）
            cursor.execute(f"DROP DATABASE IF EXISTS {Config.DB_NAME}")
            # 创建新数据库
            cursor.execute(f"CREATE DATABASE {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ 数据库 '{Config.DB_NAME}' 创建成功")
        connection.commit()
    finally:
        connection.close()
def create_tables():
    """创建所有表"""
    connection = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # 1. Users 表
            cursor.execute("""
                CREATE TABLE users (
                    user_id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    user_type ENUM('admin', 'principal', 'school_admin', 'teacher', 
                                   'student', 'community_chair', 'community_member', 'public') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL,
                    INDEX idx_user_type (user_type),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 users 表")
            
            # 2. Organizations 表
            cursor.execute("""
                CREATE TABLE organizations (
                    org_id INT PRIMARY KEY AUTO_INCREMENT,
                    org_type ENUM('school', 'community') NOT NULL,
                    org_name VARCHAR(200) NOT NULL,
                    org_profile TEXT,
                    is_public BOOLEAN DEFAULT TRUE,
                    subscription_status ENUM('active', 'inactive', 'pending') DEFAULT 'pending',
                    subscription_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_org_type (org_type),
                    INDEX idx_subscription_status (subscription_status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 organizations 表")
            
            # 3. Organization_Members 表
            cursor.execute("""
                CREATE TABLE organization_members (
                    membership_id INT PRIMARY KEY AUTO_INCREMENT,
                    org_id INT NOT NULL,
                    user_id INT NOT NULL,
                    role ENUM('principal', 'admin', 'teacher', 'student', 'chairman', 'member') NOT NULL,
                    access_code VARCHAR(50) UNIQUE,
                    joined_date DATE NOT NULL,
                    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE KEY unique_org_user (org_id, user_id),
                    INDEX idx_role (role)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 organization_members 表")
            
            # 4. Classes 表
            cursor.execute("""
                CREATE TABLE classes (
                    class_id INT PRIMARY KEY AUTO_INCREMENT,
                    org_id INT NOT NULL,
                    teacher_id INT NOT NULL,
                    class_name VARCHAR(100) NOT NULL,
                    syllabus TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
                    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_teacher (teacher_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 classes 表")
            
            # 5. Class_Enrollments 表
            cursor.execute("""
                CREATE TABLE class_enrollments (
                    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
                    class_id INT NOT NULL,
                    student_id INT NOT NULL,
                    enrollment_date DATE NOT NULL,
                    status ENUM('active', 'inactive') DEFAULT 'active',
                    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
                    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE KEY unique_class_student (class_id, student_id),
                    INDEX idx_student (student_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 class_enrollments 表")
            
            # 6. Programs 表
            cursor.execute("""
                CREATE TABLE programs (
                    program_id INT PRIMARY KEY AUTO_INCREMENT,
                    program_name VARCHAR(200) NOT NULL,
                    description TEXT,
                    program_type ENUM('internal', 'local', 'regional', 'national') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_program_type (program_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 programs 表")
            
            # 7. Program_Enrollments 表
            cursor.execute("""
                CREATE TABLE program_enrollments (
                    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
                    program_id INT NOT NULL,
                    user_id INT,
                    org_id INT,
                    enrollment_date DATE NOT NULL,
                    status ENUM('active', 'completed', 'dropped') DEFAULT 'active',
                    FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
                    CHECK (user_id IS NOT NULL OR org_id IS NOT NULL),
                    INDEX idx_program (program_id),
                    INDEX idx_user (user_id),
                    INDEX idx_org (org_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 program_enrollments 表")
            
            # 8. Activities 表
            cursor.execute("""
                CREATE TABLE activities (
                    activity_id INT PRIMARY KEY AUTO_INCREMENT,
                    program_id INT NOT NULL,
                    class_id INT,
                    activity_name VARCHAR(200) NOT NULL,
                    activity_type ENUM('in-class', 'outdoor', 'challenge', 'game', 'assessment') NOT NULL,
                    description TEXT,
                    created_by INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
                    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
                    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_program (program_id),
                    INDEX idx_class (class_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 activities 表")
            
            # 9. Content_Library 表
            cursor.execute("""
                CREATE TABLE content_library (
                    content_id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(300) NOT NULL,
                    content_type ENUM('article', 'essay', 'report', 'sighting', 'photo', 
                                     'video', 'educational_material') NOT NULL,
                    content_data TEXT,
                    created_by INT NOT NULL,
                    org_id INT,
                    is_public BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (org_id) REFERENCES organizations(org_id) ON DELETE CASCADE,
                    INDEX idx_content_type (content_type),
                    INDEX idx_org (org_id),
                    INDEX idx_public (is_public)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 content_library 表")
            
            # 10. Species_Sightings 表
            cursor.execute("""
                CREATE TABLE species_sightings (
                    sighting_id INT PRIMARY KEY AUTO_INCREMENT,
                    species_name VARCHAR(100) NOT NULL,
                    location VARCHAR(200) NOT NULL,
                    date_time DATETIME NOT NULL,
                    description TEXT,
                    photo_path VARCHAR(500),
                    reported_by INT NOT NULL,
                    verified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (reported_by) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_species (species_name),
                    INDEX idx_reporter (reported_by),
                    INDEX idx_verified (verified)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 species_sightings 表")
            
            # 11. Submissions 表
            cursor.execute("""
                CREATE TABLE submissions (
                    submission_id INT PRIMARY KEY AUTO_INCREMENT,
                    activity_id INT NOT NULL,
                    student_id INT NOT NULL,
                    submission_data TEXT,
                    submission_file_path VARCHAR(500),
                    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status ENUM('submitted', 'graded', 'returned') DEFAULT 'submitted',
                    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE,
                    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_activity (activity_id),
                    INDEX idx_student (student_id),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 submissions 表")
            
            # 12. Assessments 表
            cursor.execute("""
                CREATE TABLE assessments (
                    assessment_id INT PRIMARY KEY AUTO_INCREMENT,
                    submission_id INT NOT NULL,
                    teacher_id INT NOT NULL,
                    grade VARCHAR(10),
                    feedback TEXT,
                    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id) ON DELETE CASCADE,
                    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE KEY unique_submission (submission_id),
                    INDEX idx_teacher (teacher_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 assessments 表")
            
            # 13. Messages 表
            cursor.execute("""
                CREATE TABLE messages (
                    message_id INT PRIMARY KEY AUTO_INCREMENT,
                    sender_id INT NOT NULL,
                    recipient_id INT NOT NULL,
                    message_text TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    read_at TIMESTAMP NULL,
                    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (recipient_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_sender (sender_id),
                    INDEX idx_recipient (recipient_id),
                    INDEX idx_read (read_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 messages 表")
            
            # 14. Notes 表
            cursor.execute("""
                CREATE TABLE notes (
                    note_id INT PRIMARY KEY AUTO_INCREMENT,
                    teacher_id INT NOT NULL,
                    target_type ENUM('submission', 'content', 'sighting') NOT NULL,
                    target_id INT NOT NULL,
                    note_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_teacher (teacher_id),
                    INDEX idx_target (target_type, target_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 notes 表")
            
            # 15. User_Profiles 表
            cursor.execute("""
                CREATE TABLE user_profiles (
                    profile_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    avatar_path VARCHAR(500),
                    color_scheme VARCHAR(50),
                    bio TEXT,
                    is_public BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user (user_id),
                    INDEX idx_public (is_public)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 user_profiles 表")
            
            # 16. Creative_Canvas 表
            cursor.execute("""
                CREATE TABLE creative_canvas (
                    canvas_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    program_id INT NOT NULL,
                    assets JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
                    INDEX idx_user (user_id),
                    INDEX idx_program (program_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 creative_canvas 表")
            
            # 17. Access_Logs 表
            cursor.execute("""
                CREATE TABLE access_logs (
                    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT,
                    action VARCHAR(200) NOT NULL,
                    target_type VARCHAR(50),
                    target_id INT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address VARCHAR(45),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
                    INDEX idx_user (user_id),
                    INDEX idx_timestamp (timestamp),
                    INDEX idx_action (action)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 access_logs 表")
            
            # 18. Business_Analytics 表
            cursor.execute("""
                CREATE TABLE business_analytics (
                    analytics_id INT PRIMARY KEY AUTO_INCREMENT,
                    metric_type VARCHAR(100) NOT NULL,
                    metric_value DECIMAL(15,2),
                    metric_data JSON,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_metric_type (metric_type),
                    INDEX idx_recorded_at (recorded_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ 创建 business_analytics 表")
            
        connection.commit()
        print("\n✓ 所有表创建成功！")
    finally:
        connection.close()

def insert_initial_data():
    """插入初始数据"""
    connection = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            print("\n开始插入初始数据...")
            
            # 1. 插入用户
            users_data = [
                # 系统管理员
                ('asnawi', 'asnawi@komodo.org', hash_password('admin123'), 'admin'),
                
                # 学校相关用户
                ('khairunnisa', 'khairunnisa@ujungraya.sch.id', hash_password('principal123'), 'principal'),
                ('ayu_lestari', 'ayu@ujungraya.sch.id', hash_password('admin123'), 'school_admin'),
                ('bintang_akbar', 'bintang@ujungraya.sch.id', hash_password('teacher123'), 'teacher'),
                ('maya_sari', 'maya@ujungraya.sch.id', hash_password('teacher123'), 'teacher'),
                ('student1', 'student1@ujungraya.sch.id', hash_password('student123'), 'student'),
                ('student2', 'student2@ujungraya.sch.id', hash_password('student123'), 'student'),
                ('student3', 'student3@ujungraya.sch.id', hash_password('student123'), 'student'),
                ('student4', 'student4@ujungraya.sch.id', hash_password('student123'), 'student'),
                ('student5', 'student5@ujungraya.sch.id', hash_password('student123'), 'student'),
                
                # 社区相关用户
                ('besoeki_rachmat', 'besoeki@saveouranimals.org', hash_password('chair123'), 'community_chair'),
                ('community_member1', 'member1@saveouranimals.org', hash_password('member123'), 'community_member'),
                ('community_member2', 'member2@saveouranimals.org', hash_password('member123'), 'community_member'),
                ('community_member3', 'member3@saveouranimals.org', hash_password('member123'), 'community_member'),
                
                # 管理团队
                ('tegar_prayudi', 'tegar@komodo.org', hash_password('director123'), 'admin'),
                ('bhaskara', 'bhaskara@komodo.org', hash_password('security123'), 'admin'),
            ]
            
            cursor.executemany("""
                INSERT INTO users (username, email, password_hash, user_type)
                VALUES (%s, %s, %s, %s)
            """, users_data)
            print(f"✓ 插入 {len(users_data)} 个用户")
            
            # 2. 插入组织
            organizations_data = [
                ('school', 'Ujung Raya Primary School', 
                 'Located in Ujung Kulon, conservation area for Javan Rhinoceros', 
                 True, 'active', date(2024, 1, 15)),
                ('community', '#SaveOurAnimals Community', 
                 'Established in 2011, one of the biggest animal conservation communities in Indonesia', 
                 True, 'active', date(2024, 2, 1)),
                ('school', 'Jakarta Green School',
                 'Urban school focused on environmental education',
                 True, 'active', date(2024, 3, 1)),
            ]
            
            cursor.executemany("""
                INSERT INTO organizations (org_type, org_name, org_profile, is_public, 
                                          subscription_status, subscription_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, organizations_data)
            print(f"✓ 插入 {len(organizations_data)} 个组织")
            
            # 3. 插入组织成员
            org_members_data = [
                # Ujung Raya Primary School (org_id=1)
                (1, 2, 'principal', None, date(2024, 1, 15)),  # Khairunnisa
                (1, 3, 'admin', None, date(2024, 1, 15)),      # Ayu Lestari
                (1, 4, 'teacher', None, date(2024, 1, 20)),    # Bintang Akbar
                (1, 5, 'teacher', None, date(2024, 1, 20)),    # Maya Sari
                (1, 6, 'student', 'STU-2024-001', date(2024, 2, 1)),  # Student 1
                (1, 7, 'student', 'STU-2024-002', date(2024, 2, 1)),  # Student 2
                (1, 8, 'student', 'STU-2024-003', date(2024, 2, 1)),  # Student 3
                (1, 9, 'student', 'STU-2024-004', date(2024, 2, 1)),  # Student 4
                (1, 10, 'student', 'STU-2024-005', date(2024, 2, 1)), # Student 5
                
                # #SaveOurAnimals Community (org_id=2)
                (2, 11, 'chairman', None, date(2024, 2, 1)),   # Besoeki
                (2, 12, 'member', None, date(2024, 2, 5)),     # Member 1
                (2, 13, 'member', None, date(2024, 2, 10)),    # Member 2
                (2, 14, 'member', None, date(2024, 2, 15)),    # Member 3
            ]
            
            cursor.executemany("""
                INSERT INTO organization_members (org_id, user_id, role, access_code, joined_date)
                VALUES (%s, %s, %s, %s, %s)
            """, org_members_data)
            print(f"✓ 插入 {len(org_members_data)} 个组织成员关系")
            
            # 4. 插入保护项目
            programs_data = [
                ('Javan Rhinoceros Protection', 
                 'Conservation program for critically endangered Javan Rhinoceros in Ujung Kulon National Park',
                 'regional'),
                ('Sumatran Tiger Conservation',
                 'Protection and habitat preservation for Sumatran Tigers',
                 'national'),
                ('Bali Myna Recovery',
                 'Breeding and release program for Bali Myna (Jalak Bali)',
                 'regional'),
                ('Indonesian Wildlife Education',
                 'Educational program about Indonesian endangered species for schools',
                 'national'),
                ('Community-Based Conservation',
                 'Engaging local communities in conservation efforts',
                 'local'),
            ]
            
            cursor.executemany("""
                INSERT INTO programs (program_name, description, program_type)
                VALUES (%s, %s, %s)
            """, programs_data)
            print(f"✓ 插入 {len(programs_data)} 个保护项目")
            
            # 5. 插入班级
            classes_data = [
                (1, 4, 'Conservation Biology Class A', 
                 'Introduction to conservation principles and endangered species'),
                (1, 4, 'Javan Rhino Project',
                 'Hands-on project focused on local Javan Rhinoceros conservation'),
                (1, 5, 'Wildlife Photography',
                 'Learning to document wildlife through photography'),
            ]
            
            cursor.executemany("""
                INSERT INTO classes (org_id, teacher_id, class_name, syllabus)
                VALUES (%s, %s, %s, %s)
            """, classes_data)
            print(f"✓ 插入 {len(classes_data)} 个班级")
            
            # 6. 插入班级注册
            class_enrollments_data = [
                # Conservation Biology Class A
                (1, 6, date(2024, 2, 1), 'active'),
                (1, 7, date(2024, 2, 1), 'active'),
                (1, 8, date(2024, 2, 1), 'active'),
                
                # Javan Rhino Project
                (2, 6, date(2024, 2, 5), 'active'),
                (2, 7, date(2024, 2, 5), 'active'),
                (2, 9, date(2024, 2, 5), 'active'),
                (2, 10, date(2024, 2, 5), 'active'),
                
                # Wildlife Photography
                (3, 8, date(2024, 2, 10), 'active'),
                (3, 9, date(2024, 2, 10), 'active'),
                (3, 10, date(2024, 2, 10), 'active'),
            ]
            
            cursor.executemany("""
                INSERT INTO class_enrollments (class_id, student_id, enrollment_date, status)
                VALUES (%s, %s, %s, %s)
            """, class_enrollments_data)
            print(f"✓ 插入 {len(class_enrollments_data)} 个班级注册记录")
            
            # 7. 插入项目注册
            program_enrollments_data = [
                # 学校注册项目
                (1, None, 1, date(2024, 2, 1), 'active'),  # Javan Rhino
                (4, None, 1, date(2024, 2, 1), 'active'),  # Wildlife Education
                
                # 社区注册项目
                (5, None, 2, date(2024, 2, 1), 'active'),  # Community Conservation
                (2, None, 2, date(2024, 2, 1), 'active'),  # Sumatran Tiger
                
                # 个人用户注册
                (1, 12, None, date(2024, 2, 5), 'active'),
                (2, 13, None, date(2024, 2, 10), 'active'),
            ]
            
            cursor.executemany("""
                INSERT INTO program_enrollments (program_id, user_id, org_id, enrollment_date, status)
                VALUES (%s, %s, %s, %s, %s)
            """, program_enrollments_data)
            print(f"✓ 插入 {len(program_enrollments_data)} 个项目注册记录")
            
            # 8. 插入活动
            activities_data = [
                (1, 1, 'Rhino Habitat Study', 'in-class', 
                 'Study the habitat requirements of Javan Rhinoceros', 4),
                (1, 2, 'Field Trip to Ujung Kulon', 'outdoor',
                 'Visit Ujung Kulon National Park to observe rhino habitat', 4),
                (4, None, 'Species Identification Challenge', 'challenge',
                 'Learn to identify Indonesian endangered species', 1),
                (4, 3, 'Wildlife Photography Assignment', 'assessment',
                 'Take photos of local wildlife and create a portfolio', 5),
            ]
            
            cursor.executemany("""
                INSERT INTO activities (program_id, class_id, activity_name, activity_type, 
                                       description, created_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, activities_data)
            print(f"✓ 插入 {len(activities_data)} 个活动")
            
            # 9. 插入用户资料
            user_profiles_data = [
                # 学生资料（不公开）
                (6, '/avatars/student1.png', 'blue', 'I love rhinos!', False),
                (7, '/avatars/student2.png', 'green', 'Future conservationist', False),
                (8, '/avatars/student3.png', 'orange', 'Wildlife photographer', False),
                (9, '/avatars/student4.png', 'purple', 'Nature lover', False),
                (10, '/avatars/student5.png', 'red', 'Animal friend', False),
                
                # 社区成员资料（公开）
                (11, '/avatars/besoeki.png', 'brown', 
                 'Chairman of #SaveOurAnimals, passionate about wildlife conservation', True),
                (12, '/avatars/member1.png', 'teal',
                 'Wildlife photographer and conservationist', True),
                (13, '/avatars/member2.png', 'olive',
                 'Environmental educator', True),
                (14, '/avatars/member3.png', 'navy',
                 'Field researcher', True),
                
                # 教师资料
                (4, '/avatars/bintang.png', 'gray',
                 'Teacher at Ujung Raya Primary School', True),
                (5, '/avatars/maya.png', 'pink',
                 'Wildlife photography instructor', True),
            ]
            
            cursor.executemany("""
                INSERT INTO user_profiles (user_id, avatar_path, color_scheme, bio, is_public)
                VALUES (%s, %s, %s, %s, %s)
            """, user_profiles_data)
            print(f"✓ 插入 {len(user_profiles_data)} 个用户资料")
            
            # 10. 插入内容库
            content_library_data = [
                # 学校图书馆内容（学生作品）
                ('My First Rhino Sighting', 'essay', 
                 'Today I saw a Javan Rhinoceros for the first time...', 
                 6, 1, True),
                ('Conservation Report', 'report',
                 'Research on Javan Rhino population trends', 
                 7, 1, True),
                 
                # 社区图书馆内容
                ('Protecting Sumatran Tigers', 'article',
                 'Comprehensive guide to Sumatran Tiger conservation...', 
                 12, 2, True),
                ('Wildlife Photography Tips', 'article',
                 'Best practices for photographing endangered species...', 
                 13, 2, True),
                 
                # 教育材料（公开）
                ('Indonesian Endangered Species Guide', 'educational_material',
                 'Complete guide to all endangered endemic species in Indonesia...',
                 1, None, True),
            ]
            
            cursor.executemany("""
                INSERT INTO content_library (title, content_type, content_data, 
                                            created_by, org_id, is_public)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, content_library_data)
            print(f"✓ 插入 {len(content_library_data)} 个内容库条目")
            
            # 11. 插入物种目击
            species_sightings_data = [
                ('Javan Rhinoceros', 'Ujung Kulon National Park, Sector A',
                 datetime(2024, 3, 15, 8, 30), 
                 'Observed adult rhino near water source, appeared healthy',
                 '/photos/rhino_sighting_001.jpg', 6, True),
                ('Bali Myna', 'Bali Barat National Park',
                 datetime(2024, 3, 10, 14, 15),
                 'Pair of Bali Mynas spotted in nesting area',
                 '/photos/myna_sighting_001.jpg', 12, True),
                ('Sumatran Tiger', 'Leuser Ecosystem',
                 datetime(2024, 2, 28, 6, 45),
                 'Tiger tracks and signs observed during patrol',
                 None, 13, False),
            ]
            
            cursor.executemany("""
                INSERT INTO species_sightings (species_name, location, date_time, 
                                              description, photo_path, reported_by, verified)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, species_sightings_data)
            print(f"✓ 插入 {len(species_sightings_data)} 个物种目击记录")
            
            # 12. 插入作业提交
            submissions_data = [
                (1, 6, 'Rhinos need large territories with water sources...', 
                 '/submissions/student1_habitat.pdf', 'submitted'),
                (1, 7, 'The ideal habitat for Javan Rhino includes...', 
                 '/submissions/student2_habitat.pdf', 'graded'),
                (4, 8, 'My wildlife photography portfolio...',
                 '/submissions/student3_photos.zip', 'submitted'),
            ]
            
            cursor.executemany("""
                INSERT INTO submissions (activity_id, student_id, submission_data, 
                                        submission_file_path, status)
                VALUES (%s, %s, %s, %s, %s)
            """, submissions_data)
            print(f"✓ 插入 {len(submissions_data)} 个作业提交")
            
            # 13. 插入评估
            assessments_data = [
                (2, 4, 'A', 'Excellent work! Your analysis of rhino habitat is thorough.'),
            ]
            
            cursor.executemany("""
                INSERT INTO assessments (submission_id, teacher_id, grade, feedback)
                VALUES (%s, %s, %s, %s)
            """, assessments_data)
            print(f"✓ 插入 {len(assessments_data)} 个评估记录")
            
            # 14. 插入消息
            messages_data = [
                (4, 6, 'Great job on your habitat study! Please prepare for our field trip.'),
                (6, 4, 'Thank you teacher! I am very excited about the field trip.'),
                (5, 8, 'Your photography skills are improving. Keep practicing!'),
            ]
            
            cursor.executemany("""
                INSERT INTO messages (sender_id, recipient_id, message_text)
                VALUES (%s, %s, %s)
            """, messages_data)
            print(f"✓ 插入 {len(messages_data)} 条消息")
            
            # 15. 插入笔记
            notes_data = [
                (4, 'submission', 1, 'Consider adding more details about water requirements.'),
                (4, 'sighting', 1, 'Excellent observation! Well documented.'),
            ]
            
            cursor.executemany("""
                INSERT INTO notes (teacher_id, target_type, target_id, note_text)
                VALUES (%s, %s, %s, %s)
            """, notes_data)
            print(f"✓ 插入 {len(notes_data)} 条笔记")
            
            # 16. 插入创意画布
            canvas_data = [
                (6, 1, json.dumps({
                    'achievements': ['First Rhino Sighting', 'Habitat Study Completed'],
                    'photos': ['/canvas/student1_photo1.jpg', '/canvas/student1_photo2.jpg'],
                    'essays': ['My First Rhino Sighting']
                })),
                (8, 4, json.dumps({
                    'achievements': ['Wildlife Photographer Badge'],
                    'photos': ['/canvas/student3_photo1.jpg'],
                    'portfolio': 'Wildlife Photography Portfolio'
                })),
            ]
            
            cursor.executemany("""
                INSERT INTO creative_canvas (user_id, program_id, assets)
                VALUES (%s, %s, %s)
            """, canvas_data)
            print(f"✓ 插入 {len(canvas_data)} 个创意画布")
            
            # 17. 插入业务分析数据
            analytics_data = [
                ('total_subscriptions', 3, json.dumps({'schools': 2, 'communities': 1})),
                ('active_users', 16, json.dumps({'breakdown': 'by_type'})),
                ('popular_program', 1, json.dumps({'name': 'Javan Rhinoceros Protection'})),
            ]
            
            cursor.executemany("""
                INSERT INTO business_analytics (metric_type, metric_value, metric_data)
                VALUES (%s, %s, %s)
            """, analytics_data)
            print(f"✓ 插入 {len(analytics_data)} 条业务分析数据")
            
        connection.commit()
        print("\n✓ 所有初始数据插入成功！")
        
    finally:
        connection.close()
def main():
    """主函数"""
    print("="*60)
    print("Komodo Hub 数据库初始化")
    print("="*60 + "\n")
    
    try:
        # 1. 创建数据库
        print("步骤 1: 创建数据库...")
        create_database()
        
        # 2. 创建表
        print("\n步骤 2: 创建表结构...")
        create_tables()
        
        # 3. 插入初始数据
        print("\n步骤 3: 插入初始数据...")
        insert_initial_data()
        
        # 4. 打印摘要
        print_summary()
        
        print("✓ 数据库初始化完成！")
        print("\n您现在可以启动服务器：")
        print("  python server/app.py")
        print("\n然后启动客户端：")
        print("  python client/main.py")
        
    except Exception as e:
        print(f"\n✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
