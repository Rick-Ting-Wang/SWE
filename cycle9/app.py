# app.py (Frontend code)
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import hashlib
import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
load_dotenv()


# Database connection configuration (keep consistent with backend)
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


# Utility functions (keep consistent with backend)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def log_access(user_id: Optional[int], action: str, target_type: Optional[str] = None, target_id: Optional[int] = None):
    db = Database()
    ip = request.remote_addr
    db.execute("""
               INSERT INTO access_logs (user_id, action, target_type, target_id, ip_address)
               VALUES (%s, %s, %s, %s, %s)
               """, (user_id, action, target_type, target_id, ip))
    db.close()


def require_role(user_id: int, allowed_roles: List[str]) -> bool:
    db = Database()
    row = db.execute("SELECT user_type FROM users WHERE user_id = %s", (user_id,))
    db.close()
    if not row or row[0]['user_type'] not in allowed_roles:
        return False
    return True


# Route - Home page / Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed = hash_password(password)

        db = Database()
        row = db.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed))
        db.close()

        if row:
            user = row[0]
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['user_type'] = user['user_type']

            # Update last login time
            db = Database()
            db.execute("UPDATE users SET last_login = NOW() WHERE user_id = %s", (user['user_id'],))
            db.close()

            log_access(user['user_id'], "login")
            flash(f"Login successful! Welcome {user['username']} ({user['user_type']})")
            return redirect(url_for('main_menu'))
        else:
            flash("Login failed! Invalid email or password")

    return render_template('login.html')


# Route - Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        user_type = request.form['user_type']
        image = request.form['avatar'] or '1'

        try:
            db = Database()
            db.execute("""
                       INSERT INTO users (user_image, username, email, password, user_type)
                       VALUES (%s, %s, %s, %s, %s)
                       """, (image, username, email, password, user_type))

            user_id = db.cursor.lastrowid
            db.execute("INSERT INTO user_profiles (user_id) VALUES (%s)", (user_id,))
            db.close()

            log_access(None, "register", "user", user_id)
            flash("Registration successful! Please login")
            return redirect(url_for('login'))
        except pymysql.err.IntegrityError:
            flash("Username or email already exists!")
            return render_template('register.html')

    user_types = [
        'admin', 'principal', 'school_admin',
        'teacher', 'student', 'community_chair',
        'community_member', 'public'
    ]
    return render_template('register.html', user_types=user_types)


# Route - Main menu
@app.route('/menu')
def main_menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('main_menu.html',
                           username=session['username'],
                           user_type=session['user_type'])


# Route - Organization management
@app.route('/create_organization', methods=['GET', 'POST'])
def create_organization():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if not require_role(session['user_id'], ['admin', 'principal', 'community_chair']):
        flash("Insufficient permissions!")
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        name = request.form['name']
        org_type = request.form['org_type']
        profile = request.form['profile']
        is_public = request.form.get('is_public') == 'on'

        db = Database()
        db.execute("""
                   INSERT INTO organizations (org_type, org_name, org_profile, is_public)
                   VALUES (%s, %s, %s, %s)
                   """, (org_type, name, profile or None, is_public))

        org_id = db.cursor.lastrowid
        role_map = {'principal': 'principal', 'community_chair': 'chairman'}
        role = role_map.get(session['user_type'], 'admin')

        db.execute("""
                   INSERT INTO organization_members (org_id, user_id, role, joined_date)
                   VALUES (%s, %s, %s, CURDATE())
                   """, (org_id, session['user_id'], role))
        db.close()

        log_access(session['user_id'], "create_organization", "organization", org_id)
        flash("Organization created successfully!")
        return redirect(url_for('main_menu'))

    return render_template('create_organization.html')


@app.route('/join_organization', methods=['GET', 'POST'])
def join_organization():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        org_id = int(request.form['org_id'])
        code = request.form['code'] or None

        db = Database()
        row = db.execute("SELECT * FROM organizations WHERE org_id = %s", (org_id,))

        if not row:
            db.close()
            flash("Organization does not exist!")
            return render_template('join_organization.html')

        org = row[0]
        if not org['is_public'] and code is None:
            db.close()
            flash("Access code required!")
            return render_template('join_organization.html')

        role = 'student' if org['org_type'] == 'school' else 'member'
        if org['org_type'] == 'school' and session['user_type'] == 'teacher':
            role = 'teacher'

        try:
            db.execute("""
                       INSERT INTO organization_members (org_id, user_id, role, access_code, joined_date)
                       VALUES (%s, %s, %s, %s, CURDATE())
                       """, (org_id, session['user_id'], role, code))
            db.close()
            log_access(session['user_id'], "join_organization", "organization", org_id)
            flash("Successfully joined!")
            return redirect(url_for('main_menu'))
        except pymysql.err.IntegrityError:
            db.close()
            flash("Already joined or invalid code!")

    return render_template('join_organization.html')


# Route - Course management
@app.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if not require_role(session['user_id'], ['teacher', 'school_admin']):
        flash("Insufficient permissions!")
        return redirect(url_for('main_menu'))

    db = Database()
    org_rows = db.execute("""
                          SELECT om.org_id, o.org_name
                          FROM organization_members om
                                   JOIN organizations o ON om.org_id = o.org_id
                          WHERE om.user_id = %s
                            AND o.org_type = 'school'
                          """, (session['user_id'],))
    db.close()

    if not org_rows:
        flash("You are not in any school organization!")
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        org_id = int(request.form['org_id'])
        name = request.form['name']
        syllabus = request.form['syllabus']

        db = Database()
        db.execute("""
                   INSERT INTO classes (org_id, teacher_id, class_name, syllabus)
                   VALUES (%s, %s, %s, %s)
                   """, (org_id, session['user_id'], name, syllabus))

        class_id = db.cursor.lastrowid
        db.close()
        log_access(session['user_id'], "create_class", "class", class_id)
        flash("Course created successfully!")
        return redirect(url_for('main_menu'))

    return render_template('create_class.html', organizations=org_rows)


@app.route('/enroll_class', methods=['GET', 'POST'])
def enroll_class():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        class_id = int(request.form['class_id'])

        db = Database()
        try:
            db.execute("""
                       INSERT INTO class_enrollments (class_id, student_id, enrollment_date)
                       VALUES (%s, %s, CURDATE())
                       """, (class_id, session['user_id']))
            db.close()
            log_access(session['user_id'], "enroll_class", "class", class_id)
            flash("Successfully enrolled!")
        except pymysql.err.IntegrityError:
            db.close()
            flash("Already enrolled in this course!")

    # Get available course list
    db = Database()
    classes = db.execute("""
                         SELECT c.class_id, c.class_name, o.org_name
                         FROM classes c
                                  JOIN organizations o ON c.org_id = o.org_id
                         """)
    db.close()

    return render_template('enroll_class.html', classes=classes)


# Route - Program and activity
@app.route('/create_program', methods=['GET', 'POST'])
def create_program():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if not require_role(session['user_id'], ['admin', 'principal', 'community_chair']):
        flash("Insufficient permissions!")
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        ptype = request.form['program_type']

        db = Database()
        db.execute("""
                   INSERT INTO programs (program_name, description, program_type)
                   VALUES (%s, %s, %s)
                   """, (name, desc, ptype))

        pid = db.cursor.lastrowid
        db.close()
        log_access(session['user_id'], "create_program", "program", pid)
        flash("Program created successfully!")
        return redirect(url_for('main_menu'))

    program_types = ['internal', 'local', 'regional', 'national']
    return render_template('create_program.html', program_types=program_types)


@app.route('/enroll_program', methods=['GET', 'POST'])
def enroll_program():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get available programs list
    db = Database()
    programs = db.execute("SELECT program_id, program_name FROM programs")

    # Get organizations the user belongs to
    orgs = db.execute("""
                      SELECT om.org_id, o.org_name
                      FROM organization_members om
                               JOIN organizations o ON om.org_id = o.org_id
                      WHERE om.user_id = %s
                      """, (session['user_id'],))
    db.close()

    if request.method == 'POST':
        pid = int(request.form['program_id'])
        is_org = request.form.get('is_org') == 'on'
        org_id = int(request.form['org_id']) if is_org else None

        db = Database()
        db.execute("""
                   INSERT INTO program_enrollments (program_id, user_id, org_id, enrollment_date)
                   VALUES (%s, %s, %s, CURDATE())
                   """, (pid, session['user_id'] if not is_org else None, org_id))
        db.close()

        log_access(session['user_id'], "enroll_program", "program", pid)
        flash("Successfully enrolled!")
        return redirect(url_for('main_menu'))

    return render_template('enroll_program.html', programs=programs, organizations=orgs)


@app.route('/create_activity', methods=['GET', 'POST'])
def create_activity():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if not require_role(session['user_id'], ['teacher', 'admin']):
        flash("Insufficient permissions!")
        return redirect(url_for('main_menu'))

    # Get programs list
    db = Database()
    programs = db.execute("SELECT program_id, program_name FROM programs")

    # Get courses created by user
    classes = db.execute("""
                         SELECT class_id, class_name
                         FROM classes
                         WHERE teacher_id = %s
                         """, (session['user_id'],))
    db.close()

    if request.method == 'POST':
        pid = int(request.form['program_id'])
        class_id = int(request.form['class_id']) if request.form['class_id'] else None
        name = request.form['name']
        atype = request.form['activity_type']
        desc = request.form['description']

        db = Database()
        db.execute("""
                   INSERT INTO activities (program_id, class_id, activity_name, activity_type, description, created_by)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """, (pid, class_id, name, atype, desc, session['user_id']))

        aid = db.cursor.lastrowid
        db.close()
        log_access(session['user_id'], "create_activity", "activity", aid)
        flash("Activity created successfully!")
        return redirect(url_for('main_menu'))

    activity_types = ['in-class', 'outdoor', 'challenge', 'game', 'assessment']
    return render_template('create_activity.html',
                           programs=programs,
                           classes=classes,
                           activity_types=activity_types)


# Route - Content and sightings
@app.route('/upload_content', methods=['GET', 'POST'])
def upload_content():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get organizations the user belongs to
    db = Database()
    orgs = db.execute("""
                      SELECT org_id, org_name
                      FROM organization_members om
                               JOIN organizations o ON om.org_id = o.org_id
                      WHERE om.user_id = %s
                      """, (session['user_id'],))
    db.close()

    if request.method == 'POST':
        title = request.form['title']
        ctype = request.form['content_type']
        data = request.form['content']
        org_id = int(request.form['org_id']) if request.form['org_id'] else None
        is_public = request.form.get('is_public') == 'on'

        db = Database()
        db.execute("""
                   INSERT INTO content_library (title, content_type, content_data, created_by, org_id, is_public)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """, (title, ctype, data, session['user_id'], org_id, is_public))

        cid = db.cursor.lastrowid
        db.close()
        log_access(session['user_id'], "upload_content", "content", cid)
        flash("Upload successful!")
        return redirect(url_for('main_menu'))

    content_types = [
        'article', 'essay', 'report', 'sighting',
        'photo', 'video', 'educational_material'
    ]
    return render_template('upload_content.html',
                           organizations=orgs,
                           content_types=content_types)


@app.route('/report_sighting', methods=['GET', 'POST'])
def report_sighting():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        species = request.form['species']
        location = request.form['location']
        dt = request.form['datetime']
        desc = request.form['description']
        photo = request.form['photo'] or None

        db = Database()
        db.execute("""
                   INSERT INTO species_sightings (species_name, location, date_time, description, photo_path,
                                                  reported_by)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """, (species, location, dt, desc, photo, session['user_id']))

        sid = db.cursor.lastrowid
        db.close()
        log_access(session['user_id'], "report_sighting", "sighting", sid)
        flash("Sighting reported successfully!")
        return redirect(url_for('main_menu'))

    return render_template('report_sighting.html')


# Route - Assignment submission and grading
@app.route('/submit_assignment', methods=['GET', 'POST'])
def submit_assignment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get activities the user can submit
    db = Database()
    activities = db.execute("""
                            SELECT a.activity_id, a.activity_name, p.program_name
                            FROM activities a
                                     JOIN programs p ON a.program_id = p.program_id
                            """)
    db.close()

    if request.method == 'POST':
        aid = int(request.form['activity_id'])
        data = request.form['submission']
        file_path = request.form['file_path'] or None

        db = Database()
        db.execute("""
                   INSERT INTO submissions (activity_id, student_id, submission_data, submission_file_path)
                   VALUES (%s, %s, %s, %s)
                   """, (aid, session['user_id'], data, file_path))

        sid = db.cursor.lastrowid
        db.close()
        log_access(session['user_id'], "submit_assignment", "submission", sid)
        flash("Submission successful!")
        return redirect(url_for('main_menu'))

    return render_template('submit_assignment.html', activities=activities)


@app.route('/grade_submission', methods=['GET', 'POST'])
def grade_submission():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if not require_role(session['user_id'], ['teacher', 'school_admin']):
        flash("Insufficient permissions!")
        return redirect(url_for('main_menu'))

    # Get submissions to be graded
    db = Database()
    submissions = db.execute("""
                             SELECT s.submission_id,
                                    s.activity_id,
                                    a.activity_name,
                                    s.student_id,
                                    u.username,
                                    s.submission_data
                             FROM submissions s
                                      JOIN activities a ON s.activity_id = a.activity_id
                                      JOIN users u ON s.student_id = u.user_id
                             WHERE s.status != 'graded' AND a.created_by = %s
                             """, (session['user_id'],))
    db.close()

    if request.method == 'POST':
        sub_id = int(request.form['submission_id'])
        grade = request.form['grade']
        feedback = request.form['feedback']

        db = Database()
        db.execute("""
                   INSERT INTO assessments (submission_id, teacher_id, grade, feedback)
                   VALUES (%s, %s, %s, %s)
                   """, (sub_id, session['user_id'], grade, feedback))

        db.execute("UPDATE submissions SET status = 'graded' WHERE submission_id = %s", (sub_id,))
        db.close()
        log_access(session['user_id'], "grade_submission", "submission", sub_id)
        flash("Grading completed!")
        return redirect(url_for('main_menu'))

    return render_template('grade_submission.html', submissions=submissions)


# Route - Message system
@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get user list (for choosing recipient)
    db = Database()
    users = db.execute("SELECT user_id, username, email FROM users WHERE user_id != %s", (session['user_id'],))
    db.close()

    if request.method == 'POST':
        recipient_id = int(request.form['recipient_id'])
        text = request.form['message']

        db = Database()
        db.execute("""
                   INSERT INTO messages (sender_id, recipient_id, message_text)
                   VALUES (%s, %s, %s)
                   """, (session['user_id'], recipient_id, text))
        db.close()

        log_access(session['user_id'], "send_message", "message")
        flash("Message sent successfully!")
        return redirect(url_for('main_menu'))

    return render_template('send_message.html', users=users)


# Route - Creative Canvas
@app.route('/save_canvas', methods=['GET', 'POST'])
def save_canvas():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get program list
    db = Database()
    programs = db.execute("SELECT program_id, program_name FROM programs")
    db.close()

    if request.method == 'POST':
        pid = int(request.form['program_id'])
        assets = request.form['assets']

        db = Database()
        db.execute("""
                   INSERT INTO creative_canvas (user_id, program_id, assets)
                   VALUES (%s, %s, %s) ON DUPLICATE KEY
                   UPDATE assets = %s, updated_at = NOW()
                   """, (session['user_id'], pid, assets, assets))
        db.close()

        flash("Canvas saved successfully!")
        return redirect(url_for('main_menu'))

    return render_template('save_canvas.html', programs=programs)


# Route - Analytics
@app.route('/record_analytics', methods=['GET', 'POST'])
def record_analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if not require_role(session['user_id'], ['admin']):
        flash("Insufficient permissions!")
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        mtype = request.form['metric_type']
        value = float(request.form['value'])
        data = request.form['data'] or None

        db = Database()
        db.execute("""
                   INSERT INTO business_analytics (metric_type, metric_value, metric_data)
                   VALUES (%s, %s, %s)
                   """, (mtype, value, data))
        db.close()

        flash("Recorded successfully!")
        return redirect(url_for('main_menu'))

    return render_template('record_analytics.html')


# Route - Logout
@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_access(session['user_id'], "logout")
        session.clear()
        flash("Logged out successfully!")
    return redirect(url_for('login'))


# Route - User Center
@app.route('/user_center')
def user_center():
    # 1. Check login status
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 2. Automatically create avatar directory (to avoid missing image path)
    avatar_dir = os.path.join(app.root_path, 'avatar')
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)

    # 3. Get user's basic information (join users and user_profiles tables)
    db = Database()
    user_info = db.execute("""
                           SELECT u.user_id,
                                  u.username,
                                  u.email,
                                  u.user_type,
                                  u.user_image,
                                  u.created_at,
                                  u.last_login,
                                  p.avatar_path,
                                  p.color_scheme,
                                  p.bio,
                                  p.is_public
                           FROM users u
                                    LEFT JOIN user_profiles p ON u.user_id = p.user_id
                           WHERE u.user_id = %s
                           """, (session['user_id'],))[0]  # Get the first record (user is unique)

    # 4. Assemble avatar path (points to avatar/1.jpg~9.jpg under avatar directory)
    # Example: app.py at the same level directory /avatar/1.jpg
    user_info['avatar_url'] = url_for('static', filename=f"avatar/{user_info['user_image']}.jpg")

    # 5. Get user's received messages (ordered by send time desc, latest first)
    received_messages = db.execute("""
                                   SELECT m.message_id,
                                          m.message_text,
                                          m.sent_at,
                                          u.username AS sender_name,
                                          u.user_id  AS sender_id
                                   FROM messages m
                                            LEFT JOIN users u ON m.sender_id = u.user_id
                                   WHERE m.recipient_id = %s
                                   ORDER BY m.sent_at DESC
                                   """, (session['user_id'],))
    db.close()

    # 6. Pass data to frontend page
    return render_template('user_center.html',
                           user=user_info,
                           received_messages=received_messages)



if __name__ == '__main__':
    # Create templates folder if not exists
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app.run(debug=True)
