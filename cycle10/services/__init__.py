"""
Service layer for business logic
"""
import hashlib
from typing import Optional, List, Dict, Any
from models import DatabaseManager
from models.user_models import UserModel, OrganizationModel, MessageModel
from models.education_models import ClassModel, ProgramModel, ActivityModel, SubmissionModel
from models.content_models import ContentModel, SightingModel, AnalyticsModel, CanvasModel


class AuthService:
    """Authentication service"""

    def __init__(self, db_manager: DatabaseManager):
        self.user_model = UserModel(db_manager)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        hashed_password = self.hash_password(password)
        user = self.user_model.get_user_by_email(email)

        if user and user['password'] == hashed_password:
            # Update last login
            self.user_model.update_last_login(user['user_id'])
            return user
        return None

    def register_user(self, username: str, email: str, password: str,
                     user_type: str, user_image: str = '1') -> Optional[int]:
        """Register new user"""
        try:
            hashed_password = self.hash_password(password)
            user_id = self.user_model.create_user(
                username, email, hashed_password, user_type, user_image
            )
            return user_id
        except Exception:
            return None


class UserService:
    """User service for user-related operations"""

    def __init__(self, db_manager: DatabaseManager):
        self.user_model = UserModel(db_manager)
        self.message_model = MessageModel(db_manager)

    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get complete user profile"""
        profile = self.user_model.get_user_profile(user_id)
        if profile:
            # Add avatar URL
            profile['avatar_url'] = f"/static/avatar/{profile['user_image']}.jpg"
        return profile or {}

    def get_received_messages(self, user_id: int) -> List[Dict[str, Any]]:
        """Get messages received by user"""
        return self.message_model.get_received_messages(user_id)

    def send_message(self, sender_id: int, recipient_id: int, message_text: str) -> bool:
        """Send message to user"""
        try:
            self.message_model.send_message(sender_id, recipient_id, message_text)
            return True
        except Exception:
            return False


class OrganizationService:
    """Organization service for organization operations"""

    def __init__(self, db_manager: DatabaseManager):
        self.org_model = OrganizationModel(db_manager)

    def create_organization(self, org_type: str, org_name: str,
                          org_profile: Optional[str], is_public: bool,
                          creator_id: int) -> Optional[int]:
        """Create organization and add creator as member"""
        try:
            org_id = self.org_model.create_organization(
                org_type, org_name, org_profile, is_public
            )

            # Add creator as member with appropriate role
            role_map = {
                'principal': 'principal',
                'community_chair': 'chairman',
                'admin': 'admin'
            }
            role = role_map.get('admin', 'admin')  # Default to admin

            self.org_model.add_organization_member(org_id, creator_id, role)
            return org_id
        except Exception:
            return None

    def join_organization(self, org_id: int, user_id: int,
                         access_code: Optional[str] = None) -> bool:
        """Join organization"""
        try:
            # Get organization info
            orgs = self.org_model._execute_query(
                "SELECT * FROM organizations WHERE org_id = %s", (org_id,)
            )
            if not orgs:
                return False

            org = orgs[0]
            if not org['is_public'] and not access_code:
                return False

            # Determine role
            if org['org_type'] == 'school':
                role = 'teacher' if 'teacher' in 'user_type' else 'student'
            else:
                role = 'member'

            return self.org_model.add_organization_member(
                org_id, user_id, role, access_code
            )
        except Exception:
            return False


class EducationService:
    """Education service for class and program operations"""

    def __init__(self, db_manager: DatabaseManager):
        self.class_model = ClassModel(db_manager)
        self.program_model = ProgramModel(db_manager)
        self.activity_model = ActivityModel(db_manager)
        self.submission_model = SubmissionModel(db_manager)

    def create_class(self, org_id: int, teacher_id: int, class_name: str,
                    syllabus: Optional[str] = None) -> Optional[int]:
        """Create new class"""
        try:
            return self.class_model.create_class(org_id, teacher_id, class_name, syllabus)
        except Exception:
            return None

    def enroll_in_class(self, class_id: int, student_id: int) -> bool:
        """Enroll student in class"""
        return self.class_model.enroll_student(class_id, student_id)

    def create_program(self, program_name: str, description: str,
                      program_type: str) -> Optional[int]:
        """Create new program"""
        try:
            return self.program_model.create_program(program_name, description, program_type)
        except Exception:
            return None

    def enroll_in_program(self, program_id: int, user_id: Optional[int],
                         org_id: Optional[int]) -> bool:
        """Enroll in program"""
        return self.program_model.enroll_in_program(program_id, user_id, org_id)

    def create_activity(self, program_id: int, class_id: Optional[int],
                       activity_name: str, activity_type: str,
                       description: str, created_by: int) -> Optional[int]:
        """Create new activity"""
        try:
            return self.activity_model.create_activity(
                program_id, class_id, activity_name, activity_type, description, created_by
            )
        except Exception:
            return None

    def submit_assignment(self, activity_id: int, student_id: int,
                         submission_data: str, submission_file_path: Optional[str] = None) -> Optional[int]:
        """Submit assignment"""
        try:
            return self.submission_model.submit_assignment(
                activity_id, student_id, submission_data, submission_file_path
            )
        except Exception:
            return None

    def grade_submission(self, submission_id: int, teacher_id: int,
                        grade: str, feedback: str) -> bool:
        """Grade submission"""
        return self.submission_model.grade_submission(
            submission_id, teacher_id, grade, feedback
        )


class ContentService:
    """Content service for content and sighting operations"""

    def __init__(self, db_manager: DatabaseManager):
        self.content_model = ContentModel(db_manager)
        self.sighting_model = SightingModel(db_manager)
        self.analytics_model = AnalyticsModel(db_manager)
        self.canvas_model = CanvasModel(db_manager)

    def upload_content(self, title: str, content_type: str, content_data: str,
                      created_by: int, org_id: Optional[int], is_public: bool) -> Optional[int]:
        """Upload content"""
        try:
            return self.content_model.upload_content(
                title, content_type, content_data, created_by, org_id, is_public
            )
        except Exception:
            return None

    def report_sighting(self, species_name: str, location: str, date_time: str,
                       description: str, photo_path: Optional[str], reported_by: int) -> Optional[int]:
        """Report species sighting"""
        try:
            return self.sighting_model.report_sighting(
                species_name, location, date_time, description, photo_path, reported_by
            )
        except Exception:
            return None

    def record_analytics(self, metric_type: str, metric_value: float,
                        metric_data: Optional[str] = None) -> Optional[int]:
        """Record analytics"""
        try:
            return self.analytics_model.record_analytics(
                metric_type, metric_value, metric_data
            )
        except Exception:
            return None

    def save_canvas(self, user_id: int, program_id: int, assets: str) -> bool:
        """Save creative canvas"""
        return self.canvas_model.save_canvas(user_id, program_id, assets)