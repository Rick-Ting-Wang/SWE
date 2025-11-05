# komodo_backend.py
import pymysql
import hashlib
import os
import json
import sys
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# ==================== Database Connection ====================
class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='komodo',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.cursor = self.conn.cursor()

    def execute(self, query: str, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def executemany(self, query: str, params_list):
        self.cursor.executemany(query, params_list)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

db = Database()

# ==================== Utility Functions ====================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def log_access(user_id: Optional[int], action: str, target_type: Optional[str] = None, target_id: Optional[int] = None):
    ip = "127.0.0.1"  # Simulated
    db.execute("""
        INSERT INTO access_logs (user_id, action, target_type, target_id, ip_address)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, action, target_type, target_id, ip))

def require_role(user_id: int, allowed_roles: List[str]):
    row = db.execute("SELECT user_type FROM users WHERE user_id = %s", (user_id,))
    if not row or row[0]['user_type'] not in allowed_roles:
        print("Insufficient permissions!")
        return False
    return True

# ==================== User Authentication ====================
current_user = None

def login():
    global current_user
    email = input("Email: ")
    password = input("Password: ")
    hashed = hash_password(password)
    row = db.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed))
    if row:
        current_user = row[0]
        db.execute("UPDATE users SET last_login = NOW() WHERE user_id = %s", (current_user['user_id'],))
        log_access(current_user['user_id'], "login")
        print(f"Login successful! Welcome {current_user['username']} ({current_user['user_type']})")
    else:
        print("Login failed!")
        current_user = None

def register():
    print("Register new user")
    username = input("Username: ")
    email = input("Email: ")
    password = hash_password(input("Password: "))
    user_type = input("User type (admin/principal/school_admin/teacher/student/community_chair/community_member/public): ")
    image = input("Avatar (1-9): ") or '1'

    try:
        db.execute("""
            INSERT INTO users (user_image, username, email, password, user_type)
            VALUES (%s, %s, %s, %s, %s)
        """, (image, username, email, password, user_type))
        user_id = db.cursor.lastrowid
        db.execute("INSERT INTO user_profiles (user_id) VALUES (%s)", (user_id,))
        log_access(None, "register", "user", user_id)
        print("Registration successful!")
    except pymysql.err.IntegrityError:
        print("Username or email already exists!")

# ==================== Organization Management ====================
def create_organization():
    if not require_role(current_user['user_id'], ['admin', 'principal', 'community_chair']): return
    name = input("Organization name: ")
    org_type = input("Type (school/community): ")
    profile = input("Description (optional): ")
    is_public = input("Public (1/0): ") == '1'
    db.execute("""
        INSERT INTO organizations (org_type, org_name, org_profile, is_public)
        VALUES (%s, %s, %s, %s)
    """, (org_type, name, profile or None, is_public))
    org_id = db.cursor.lastrowid
    role_map = {'principal': 'principal', 'community_chair': 'chairman'}
    role = role_map.get(current_user['user_type'], 'admin')
    db.execute("""
        INSERT INTO organization_members (org_id, user_id, role, joined_date)
        VALUES (%s, %s, %s, CURDATE())
    """, (org_id, current_user['user_id'], role))
    log_access(current_user['user_id'], "create_organization", "organization", org_id)
    print("Organization created successfully!")

def join_organization():
    org_id = int(input("Organization ID: "))
    code = input("Access code (if any): ") or None
    row = db.execute("SELECT * FROM organizations WHERE org_id = %s", (org_id,))
    if not row:
        print("Organization does not exist!")
        return
    org = row[0]
    if not org['is_public'] and code is None:
        print("Access code required!")
        return

    role = 'student' if org['org_type'] == 'school' else 'member'
    if org['org_type'] == 'school' and current_user['user_type'] == 'teacher':
        role = 'teacher'

    try:
        db.execute("""
            INSERT INTO organization_members (org_id, user_id, role, access_code, joined_date)
            VALUES (%s, %s, %s, %s, CURDATE())
        """, (org_id, current_user['user_id'], role, code))
        log_access(current_user['user_id'], "join_organization", "organization", org_id)
        print("Successfully joined!")
    except pymysql.err.IntegrityError:
        print("Already joined or invalid code!")

# ==================== Course Management ====================
def create_class():
    if not require_role(current_user['user_id'], ['teacher', 'school_admin']): return
    org_rows = db.execute("""
        SELECT om.org_id FROM organization_members om
        JOIN organizations o ON om.org_id = o.org_id
        WHERE om.user_id = %s AND o.org_type = 'school'
    """, (current_user['user_id'],))
    if not org_rows:
        print("You are not in any school organization!")
        return
    org_id = org_rows[0]['org_id']
    name = input("Course name: ")
    syllabus = input("Course syllabus: ")
    db.execute("""
        INSERT INTO classes (org_id, teacher_id, class_name, syllabus)
        VALUES (%s, %s, %s, %s)
    """, (org_id, current_user['user_id'], name, syllabus))
    class_id = db.cursor.lastrowid
    log_access(current_user['user_id'], "create_class", "class", class_id)
    print("Course created successfully!")

def enroll_class():
    class_id = int(input("Course ID: "))
    db.execute("""
        INSERT INTO class_enrollments (class_id, student_id, enrollment_date)
        VALUES (%s, %s, CURDATE())
    """, (class_id, current_user['user_id']))
    log_access(current_user['user_id'], "enroll_class", "class", class_id)
    print("Successfully enrolled!")

# ==================== Programs and Activities ====================
def create_program():
    if not require_role(current_user['user_id'], ['admin', 'principal', 'community_chair']): return
    name = input("Program name: ")
    desc = input("Description: ")
    ptype = input("Type (internal/local/regional/national): ")
    db.execute("""
        INSERT INTO programs (program_name, description, program_type)
        VALUES (%s, %s, %s)
    """, (name, desc, ptype))
    pid = db.cursor.lastrowid
    log_access(current_user['user_id'], "create_program", "program", pid)
    print("Program created successfully!")

def enroll_program():
    pid = int(input("Program ID: "))
    is_org = input("Enroll as organization? (y/n): ") == 'y'
    org_id = None
    if is_org:
        org_id = int(input("Organization ID: "))
    db.execute("""
        INSERT INTO program_enrollments (program_id, user_id, org_id, enrollment_date)
        VALUES (%s, %s, %s, CURDATE())
    """, (pid, current_user['user_id'] if not is_org else None, org_id))
    log_access(current_user['user_id'], "enroll_program", "program", pid)
    print("Successfully enrolled!")

def create_activity():
    if not require_role(current_user['user_id'], ['teacher', 'admin']): return
    pid = int(input("Program ID: "))
    class_id = input("Associated course ID (optional): ")
    class_id = int(class_id) if class_id else None
    name = input("Activity name: ")
    atype = input("Type (in-class/outdoor/challenge/game/assessment): ")
    desc = input("Description: ")
    db.execute("""
        INSERT INTO activities (program_id, class_id, activity_name, activity_type, description, created_by)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (pid, class_id, name, atype, desc, current_user['user_id']))
    aid = db.cursor.lastrowid
    log_access(current_user['user_id'], "create_activity", "activity", aid)
    print("Activity created successfully!")

# ==================== Content and Observations ====================
def upload_content():
    title = input("Title: ")
    ctype = input("Type (article/essay/report/sighting/photo/video/educational_material): ")
    data = input("Content: ")
    org_id = input("Organization ID (optional): ")
    org_id = int(org_id) if org_id else None
    is_public = input("Public? (1/0): ") == '1'
    db.execute("""
        INSERT INTO content_library (title, content_type, content_data, created_by, org_id, is_public)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, ctype, data, current_user['user_id'], org_id, is_public))
    cid = db.cursor.lastrowid
    log_access(current_user['user_id'], "upload_content", "content", cid)
    print("Upload successful!")

def report_sighting():
    species = input("Species name: ")
    location = input("Location: ")
    dt = input("Time (YYYY-MM-DD HH:MM): ")
    desc = input("Description: ")
    photo = input("Photo path (optional): ")
    db.execute("""
        INSERT INTO species_sightings (species_name, location, date_time, description, photo_path, reported_by)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (species, location, dt, desc, photo or None, current_user['user_id']))
    sid = db.cursor.lastrowid
    log_access(current_user['user_id'], "report_sighting", "sighting", sid)
    print("Sighting reported successfully!")

# ==================== Assignment Submission and Grading ====================
def submit_assignment():
    aid = int(input("Activity ID: "))
    data = input("Submission content: ")
    file_path = input("File path (optional): ")
    db.execute("""
        INSERT INTO submissions (activity_id, student_id, submission_data, submission_file_path)
        VALUES (%s, %s, %s, %s)
    """, (aid, current_user['user_id'], data, file_path or None))
    sid = db.cursor.lastrowid
    log_access(current_user['user_id'], "submit_assignment", "submission", sid)
    print("Submission successful!")

def grade_submission():
    if not require_role(current_user['user_id'], ['teacher', 'school_admin']): return
    sub_id = int(input("Submission ID: "))
    grade = input("Grade (A/90): ")
    feedback = input("Feedback: ")
    db.execute("""
        INSERT INTO assessments (submission_id, teacher_id, grade, feedback)
        VALUES (%s, %s, %s, %s)
    """, (sub_id, current_user['user_id'], grade, feedback))
    db.execute("UPDATE submissions SET status = 'graded' WHERE submission_id = %s", (sub_id,))
    log_access(current_user['user_id'], "grade_submission", "submission", sub_id)
    print("Grading completed!")

# ==================== Messaging System ====================
def send_message():
    recipient = input("Recipient's email: ")
    row = db.execute("SELECT user_id FROM users WHERE email = %s", (recipient,))
    if not row:
        print("User does not exist!")
        return
    rid = row[0]['user_id']
    text = input("Message content: ")
    db.execute("""
        INSERT INTO messages (sender_id, recipient_id, message_text)
        VALUES (%s, %s, %s)
    """, (current_user['user_id'], rid, text))
    log_access(current_user['user_id'], "send_message", "message")
    print("Message sent successfully!")

# ==================== Creative Canvas ====================
def save_canvas():
    pid = int(input("Program ID: "))
    assets = input("JSON asset configuration: ")
    db.execute("""
        INSERT INTO creative_canvas (user_id, program_id, assets)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE assets = %s, updated_at = NOW()
    """, (current_user['user_id'], pid, assets, assets))
    print("Canvas saved successfully!")

# ==================== Analytics ====================
def record_analytics():
    if not require_role(current_user['user_id'], ['admin']): return
    mtype = input("Metric type: ")
    value = float(input("Value: "))
    data = input("Extended JSON (optional): ")
    db.execute("""
        INSERT INTO business_analytics (metric_type, metric_value, metric_data)
        VALUES (%s, %s, %s)
    """, (mtype, value, data or None))
    print("Recorded successfully!")

# ==================== Main Menu ====================
def main_menu():
    while True:
        if not current_user:
            print("\n=== Not logged in ===")
            choice = input("1.Login 2.Register 3.Exit\n> ")
            if choice == '1': login()
            elif choice == '2': register()
            elif choice == '3': break
            continue

        print(f"\n=== {current_user['username']} ({current_user['user_type']}) ===")
        menu = [
            "1. Create organization", "2. Join organization", "3. Create course", "4. Enroll in course",
            "5. Create program", "6. Enroll in program", "7. Create activity", "8. Upload content",
            "9. Report species sighting", "10. Submit assignment", "11. Grade submission", "12. Send message",
            "13. Save creative canvas", "14. Record analytics", "15. Logout", "16. Exit"
        ]
        for item in menu:
            print(item)
        choice = input("> ")

        actions = {
            '1': create_organization,
            '2': join_organization,
            '3': create_class,
            '4': enroll_class,
            '5': create_program,
            '6': enroll_program,
            '7': create_activity,
            '8': upload_content,
            '9': report_sighting,
            '10': submit_assignment,
            '11': grade_submission,
            '12': send_message,
            '13': save_canvas,
            '14': record_analytics,
            '15': lambda: globals().update(current_user=None) or print("Logged out"),
            '16': lambda: sys.exit(0)
        }
        if choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print(f"Operation failed: {e}")
        else:
            print("Invalid option!")

if __name__ == "__main__":
    print("Komodo Platform Backend Command Line System started")
    print("Please ensure the database is created and the table creation script is executed!")
    try:
        main_menu()
    finally:
        db.close()
