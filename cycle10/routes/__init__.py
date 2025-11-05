"""
Route definitions for the Flask application
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from typing import Optional
from models import DatabaseManager
from services import AuthService, UserService, OrganizationService, EducationService, ContentService
from utils import log_access, require_role, get_user_types, get_program_types, get_activity_types, get_content_types


class RouteManager:
    """Route manager for handling application routes"""

    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.db_manager = DatabaseManager(config)
        self.auth_service = AuthService(self.db_manager)
        self.user_service = UserService(self.db_manager)
        self.org_service = OrganizationService(self.db_manager)
        self.education_service = EducationService(self.db_manager)
        self.content_service = ContentService(self.db_manager)

    def register_routes(self):
        """Register all application routes"""

        @self.app.route('/', methods=['GET', 'POST'])
        def login():
            """Login route"""
            if 'user_id' in session:
                return redirect(url_for('main_menu'))

            if request.method == 'POST':
                email = request.form['email']
                password = request.form['password']

                user = self.auth_service.authenticate_user(email, password)
                if user:
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['user_type'] = user['user_type']

                    log_access(self.db_manager, user['user_id'], "login")
                    flash(f"Login successful! Welcome {user['username']} ({user['user_type']})")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Login failed! Invalid email or password")

            return render_template('login.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            """Registration route"""
            if 'user_id' in session:
                return redirect(url_for('main_menu'))

            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                user_type = request.form['user_type']
                user_image = request.form.get('avatar', '1')

                user_id = self.auth_service.register_user(
                    username, email, password, user_type, user_image
                )

                if user_id:
                    log_access(self.db_manager, None, "register", "user", user_id)
                    flash("Registration successful! Please login")
                    return redirect(url_for('login'))
                else:
                    flash("Username or email already exists!")

            return render_template('register.html', user_types=get_user_types())

        @self.app.route('/menu')
        def main_menu():
            """Main menu route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            return render_template('main_menu.html',
                                   username=session['username'],
                                   user_type=session['user_type'])

        @self.app.route('/user_center')
        def user_center():
            """User center route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            user_profile = self.user_service.get_user_profile(session['user_id'])
            received_messages = self.user_service.get_received_messages(session['user_id'])

            return render_template('user_center.html',
                                   user=user_profile,
                                   received_messages=received_messages)

        @self.app.route('/create_organization', methods=['GET', 'POST'])
        def create_organization():
            """Create organization route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if not require_role(self.db_manager, session['user_id'],
                              ['admin', 'principal', 'community_chair']):
                flash("Insufficient permissions!")
                return redirect(url_for('main_menu'))

            if request.method == 'POST':
                name = request.form['name']
                org_type = request.form['org_type']
                profile = request.form.get('profile', '')
                is_public = request.form.get('is_public') == 'on'

                org_id = self.org_service.create_organization(
                    org_type, name, profile or None, is_public, session['user_id']
                )

                if org_id:
                    log_access(self.db_manager, session['user_id'], "create_organization", "organization", org_id)
                    flash("Organization created successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to create organization!")

            return render_template('create_organization.html')

        @self.app.route('/join_organization', methods=['GET', 'POST'])
        def join_organization():
            """Join organization route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if request.method == 'POST':
                org_id = int(request.form['org_id'])
                code = request.form.get('code')

                success = self.org_service.join_organization(org_id, session['user_id'], code)
                if success:
                    log_access(self.db_manager, session['user_id'], "join_organization", "organization", org_id)
                    flash("Successfully joined!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to join organization!")

            return render_template('join_organization.html')

        @self.app.route('/create_class', methods=['GET', 'POST'])
        def create_class():
            """Create class route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if not require_role(self.db_manager, session['user_id'], ['teacher', 'school_admin']):
                flash("Insufficient permissions!")
                return redirect(url_for('main_menu'))

            # Get user's school organizations
            orgs = self.org_service.org_model.get_user_organizations(session['user_id'])
            school_orgs = [org for org in orgs if org['org_type'] == 'school']

            if not school_orgs:
                flash("You are not in any school organization!")
                return redirect(url_for('main_menu'))

            if request.method == 'POST':
                org_id = int(request.form['org_id'])
                name = request.form['name']
                syllabus = request.form.get('syllabus', '')

                class_id = self.education_service.create_class(org_id, session['user_id'], name, syllabus)
                if class_id:
                    log_access(self.db_manager, session['user_id'], "create_class", "class", class_id)
                    flash("Course created successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to create course!")

            return render_template('create_class.html', organizations=school_orgs)

        @self.app.route('/enroll_class', methods=['GET', 'POST'])
        def enroll_class():
            """Enroll in class route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if request.method == 'POST':
                class_id = int(request.form['class_id'])

                success = self.education_service.enroll_in_class(class_id, session['user_id'])
                if success:
                    log_access(self.db_manager, session['user_id'], "enroll_class", "class", class_id)
                    flash("Successfully enrolled!")
                else:
                    flash("Already enrolled in this course!")

            classes = self.education_service.class_model.get_available_classes()
            return render_template('enroll_class.html', classes=classes)

        @self.app.route('/create_program', methods=['GET', 'POST'])
        def create_program():
            """Create program route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if not require_role(self.db_manager, session['user_id'],
                              ['admin', 'principal', 'community_chair']):
                flash("Insufficient permissions!")
                return redirect(url_for('main_menu'))

            if request.method == 'POST':
                name = request.form['name']
                desc = request.form['description']
                ptype = request.form['program_type']

                program_id = self.education_service.create_program(name, desc, ptype)
                if program_id:
                    log_access(self.db_manager, session['user_id'], "create_program", "program", program_id)
                    flash("Program created successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to create program!")

            return render_template('create_program.html', program_types=get_program_types())

        @self.app.route('/enroll_program', methods=['GET', 'POST'])
        def enroll_program():
            """Enroll in program route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            programs = self.education_service.program_model.get_available_programs()
            orgs = self.org_service.org_model.get_user_organizations(session['user_id'])

            if request.method == 'POST':
                program_id = int(request.form['program_id'])
                is_org = request.form.get('is_org') == 'on'
                org_id = int(request.form['org_id']) if is_org and request.form['org_id'] else None

                success = self.education_service.enroll_in_program(
                    program_id, session['user_id'] if not is_org else None, org_id
                )
                if success:
                    log_access(self.db_manager, session['user_id'], "enroll_program", "program", program_id)
                    flash("Successfully enrolled!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to enroll in program!")

            return render_template('enroll_program.html', programs=programs, organizations=orgs)

        @self.app.route('/create_activity', methods=['GET', 'POST'])
        def create_activity():
            """Create activity route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if not require_role(self.db_manager, session['user_id'], ['teacher', 'admin']):
                flash("Insufficient permissions!")
                return redirect(url_for('main_menu'))

            programs = self.education_service.program_model.get_available_programs()
            classes = self.education_service.class_model.get_teacher_classes(session['user_id'])

            if request.method == 'POST':
                program_id = int(request.form['program_id'])
                class_id = int(request.form['class_id']) if request.form['class_id'] else None
                name = request.form['name']
                atype = request.form['activity_type']
                desc = request.form['description']

                activity_id = self.education_service.create_activity(
                    program_id, class_id, name, atype, desc, session['user_id']
                )
                if activity_id:
                    log_access(self.db_manager, session['user_id'], "create_activity", "activity", activity_id)
                    flash("Activity created successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to create activity!")

            return render_template('create_activity.html',
                                   programs=programs,
                                   classes=classes,
                                   activity_types=get_activity_types())

        @self.app.route('/submit_assignment', methods=['GET', 'POST'])
        def submit_assignment():
            """Submit assignment route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            activities = self.education_service.activity_model.get_available_activities()

            if request.method == 'POST':
                activity_id = int(request.form['activity_id'])
                data = request.form['submission']
                file_path = request.form.get('file_path')

                submission_id = self.education_service.submit_assignment(
                    activity_id, session['user_id'], data, file_path
                )
                if submission_id:
                    log_access(self.db_manager, session['user_id'], "submit_assignment", "submission", submission_id)
                    flash("Submission successful!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to submit assignment!")

            return render_template('submit_assignment.html', activities=activities)

        @self.app.route('/grade_submission', methods=['GET', 'POST'])
        def grade_submission():
            """Grade submission route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if not require_role(self.db_manager, session['user_id'], ['teacher', 'school_admin']):
                flash("Insufficient permissions!")
                return redirect(url_for('main_menu'))

            submissions = self.education_service.submission_model.get_pending_submissions(session['user_id'])

            if request.method == 'POST':
                submission_id = int(request.form['submission_id'])
                grade = request.form['grade']
                feedback = request.form['feedback']

                success = self.education_service.grade_submission(
                    submission_id, session['user_id'], grade, feedback
                )
                if success:
                    log_access(self.db_manager, session['user_id'], "grade_submission", "submission", submission_id)
                    flash("Grading completed!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to grade submission!")

            return render_template('grade_submission.html', submissions=submissions)

        @self.app.route('/upload_content', methods=['GET', 'POST'])
        def upload_content():
            """Upload content route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            orgs = self.org_service.org_model.get_user_organizations(session['user_id'])

            if request.method == 'POST':
                title = request.form['title']
                ctype = request.form['content_type']
                data = request.form['content']
                org_id = int(request.form['org_id']) if request.form['org_id'] else None
                is_public = request.form.get('is_public') == 'on'

                content_id = self.content_service.upload_content(
                    title, ctype, data, session['user_id'], org_id, is_public
                )
                if content_id:
                    log_access(self.db_manager, session['user_id'], "upload_content", "content", content_id)
                    flash("Upload successful!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to upload content!")

            return render_template('upload_content.html',
                                   organizations=orgs,
                                   content_types=get_content_types())

        @self.app.route('/report_sighting', methods=['GET', 'POST'])
        def report_sighting():
            """Report sighting route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if request.method == 'POST':
                species = request.form['species']
                location = request.form['location']
                dt = request.form['datetime']
                desc = request.form['description']
                photo = request.form.get('photo')

                sighting_id = self.content_service.report_sighting(
                    species, location, dt, desc, photo, session['user_id']
                )
                if sighting_id:
                    log_access(self.db_manager, session['user_id'], "report_sighting", "sighting", sighting_id)
                    flash("Sighting reported successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to report sighting!")

            return render_template('report_sighting.html')

        @self.app.route('/send_message', methods=['GET', 'POST'])
        def send_message():
            """Send message route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            # Get all users except current user
            users = self.user_service.user_model._execute_query(
                "SELECT user_id, username, email FROM users WHERE user_id != %s",
                (session['user_id'],)
            )

            if request.method == 'POST':
                recipient_id = int(request.form['recipient_id'])
                text = request.form['message']

                success = self.user_service.send_message(session['user_id'], recipient_id, text)
                if success:
                    log_access(self.db_manager, session['user_id'], "send_message", "message")
                    flash("Message sent successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to send message!")

            return render_template('send_message.html', users=users)

        @self.app.route('/save_canvas', methods=['GET', 'POST'])
        def save_canvas():
            """Save canvas route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            programs = self.education_service.program_model.get_available_programs()

            if request.method == 'POST':
                program_id = int(request.form['program_id'])
                assets = request.form['assets']

                success = self.content_service.save_canvas(session['user_id'], program_id, assets)
                if success:
                    flash("Canvas saved successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to save canvas!")

            return render_template('save_canvas.html', programs=programs)

        @self.app.route('/record_analytics', methods=['GET', 'POST'])
        def record_analytics():
            """Record analytics route"""
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if not require_role(self.db_manager, session['user_id'], ['admin']):
                flash("Insufficient permissions!")
                return redirect(url_for('main_menu'))

            if request.method == 'POST':
                mtype = request.form['metric_type']
                value = float(request.form['value'])
                data = request.form.get('data')

                analytics_id = self.content_service.record_analytics(mtype, value, data)
                if analytics_id:
                    flash("Recorded successfully!")
                    return redirect(url_for('main_menu'))
                else:
                    flash("Failed to record analytics!")

            return render_template('record_analytics.html')

        @self.app.route('/uno-components')
        def uno_components():
            """UnoCSS components demo route"""
            return render_template('uno-components-demo.html')

        @self.app.route('/example-unified-form')
        def example_unified_form():
            """Example unified form system demonstration"""
            try:
                # Get data for dropdowns
                user_types = get_user_types()
                # Get all public organizations
                organizations = self.db_manager.execute_query(
                    "SELECT org_id, org_name, org_type FROM organizations WHERE is_public = 1 ORDER BY org_name"
                )
                content_types = get_content_types()
            except Exception:
                # Fallback data if database is not available
                user_types = ['student', 'teacher', 'community_member', 'admin']
                organizations = [
                    {'org_id': 1, 'org_name': 'Example School', 'org_type': 'school'},
                    {'org_id': 2, 'org_name': 'Example Community', 'org_type': 'community'}
                ]
                content_types = ['article', 'video', 'image', 'document']

            return render_template('example_unified_form.html',
                                 user_types=user_types,
                                 organizations=organizations,
                                 content_types=content_types)

        @self.app.route('/logout')
        def logout():
            """Logout route"""
            if 'user_id' in session:
                log_access(self.db_manager, session['user_id'], "logout")
                session.clear()
                flash("Logged out successfully!")
            return redirect(url_for('login'))