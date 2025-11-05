"""
Komodo Hub - Service Layer and Permission Management
Service layer with business logic and permission checks
"""

from typing import Optional, List, Dict, Any
from database import db
from models.user_models import User, Organization, OrganizationMember
from models.class_models import Class, ClassEnrollment, Assessment
from models.program_models import ContentLibrary, SpeciesSighting
from models.analytics_models import AccessLog


class PermissionError(Exception):
    """Permission error exception"""
    pass


class PermissionService:
    """Permission management service"""

    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Check if user is an administrator"""
        user = User.find_by_id(user_id)
        return user and user['user_type'] == User.ADMIN

    @staticmethod
    def is_principal(user_id: int, org_id: Optional[int] = None) -> bool:
        """Check if user is a principal"""
        user = User.find_by_id(user_id)
        if not user or user['user_type'] != User.PRINCIPAL:
            return False

        if org_id:
            role = OrganizationMember.get_member_role(org_id, user_id)
            return role == OrganizationMember.PRINCIPAL

        return True

    @staticmethod
    def is_teacher(user_id: int) -> bool:
        """Check if user is a teacher"""
        user = User.find_by_id(user_id)
        return user and user['user_type'] == User.TEACHER

    @staticmethod
    def is_student(user_id: int) -> bool:
        """Check if user is a student"""
        user = User.find_by_id(user_id)
        return user and user['user_type'] == User.STUDENT

    @staticmethod
    def can_access_class(user_id: int, class_id: int) -> bool:
        """Check if user can access the class"""
        class_info = Class.find_by_id(class_id)
        if not class_info:
            return False

        # Teacher can access their own class
        if class_info['teacher_id'] == user_id:
            return True

        # Student can access class they are enrolled in
        return ClassEnrollment.check_enrollment(class_id, user_id)

    @staticmethod
    def can_access_student_data(accessor_id: int, student_id: int) -> bool:
        """Check if user can access student data (COPPA/GDPR compliance)"""
        # Student can access their own data
        if accessor_id == student_id:
            return True

        accessor = User.find_by_id(accessor_id)
        if not accessor:
            return False

        # Admin can access all data
        if accessor['user_type'] == User.ADMIN:
            AccessLog.log_action(accessor_id, 'access_student_data',
                                 'student', student_id)
            return True

        # Principal can access their own school student data
        if accessor['user_type'] == User.PRINCIPAL:
            student_orgs = User.get_user_organizations(student_id)
            accessor_orgs = User.get_user_organizations(accessor_id)

            student_org_ids = {org['org_id'] for org in student_orgs}
            accessor_org_ids = {org['org_id'] for org in accessor_orgs}

            if student_org_ids & accessor_org_ids:
                AccessLog.log_action(accessor_id, 'access_student_data',
                                     'student', student_id)
                return True

        # Teacher can only access student data from their own class
        if accessor['user_type'] == User.TEACHER:
            query = """
                    SELECT COUNT(*) as count
                    FROM class_enrollments ce
                        JOIN classes c \
                    ON ce.class_id = c.class_id
                    WHERE ce.student_id = %s \
                      AND c.teacher_id = %s \
                    """
            result = db.execute_query(query, (student_id, accessor_id))

            if result and result[0]['count'] > 0:
                AccessLog.log_action(accessor_id, 'access_student_data',
                                     'student', student_id)
                return True

        return False

    @staticmethod
    def can_view_content(user_id: Optional[int], content_id: int) -> bool:
        """Check if user can view content"""
        content = ContentLibrary.find_by_id(content_id)
        if not content:
            return False

        # Public content can be viewed by anyone
        if content['is_public']:
            return True

        # Not logged in users can only view public content
        if not user_id:
            return False

        # Content creator can view
        if content['created_by'] == user_id:
            return True

        # Members of the same organization can view (if content belongs to organization)
        if content['org_id']:
            role = OrganizationMember.get_member_role(content['org_id'], user_id)
            return role is not None

        return False

    @staticmethod
    def can_manage_organization(user_id: int, org_id: int) -> bool:
        """Check if user can manage organization"""
        role = OrganizationMember.get_member_role(org_id, user_id)
        return role in [OrganizationMember.PRINCIPAL,
                        OrganizationMember.ADMIN,
                        OrganizationMember.CHAIRMAN]


class TeacherService:
    """Teacher service"""

    @staticmethod
    def get_teacher_dashboard(teacher_id: int) -> Dict[str, Any]:
        """Get teacher dashboard data"""
        if not PermissionService.is_teacher(teacher_id):
            raise PermissionError("User is not a teacher")

        # Get teacher's classes
        classes = Class.get_teacher_classes(teacher_id)

        # Get pending submissions
        from models.class_models import Submission
        pending_submissions = Submission.get_teacher_class_submissions(teacher_id)
        pending_submissions = [s for s in pending_submissions if s['status'] == 'submitted']

        # Statistics
        total_students = 0
        for cls in classes:
            students = Class.get_class_students(cls['class_id'])
            total_students += len(students)

        dashboard = {
            'teacher_id': teacher_id,
            'total_classes': len(classes),
            'total_students': total_students,
            'pending_submissions': len(pending_submissions),
            'classes': classes,
            'recent_submissions': pending_submissions[:10]
        }

        return dashboard

    @staticmethod
    def grade_submission(teacher_id: int, submission_id: int,
                         grade: str, feedback: Optional[str] = None) -> int:
        """Teacher grades assignment"""
        from models.class_models import Submission

        # Get submission information
        submission = Submission.find_by_id(submission_id)
        if not submission:
            raise ValueError("Submission not found")

        # Check permission
        from models.class_models import Activity
        activity = Activity.find_by_id(submission['activity_id'])

        if not activity or not activity['class_id']:
            raise PermissionError("Invalid activity")

        class_info = Class.find_by_id(activity['class_id'])
        if not class_info or class_info['teacher_id'] != teacher_id:
            raise PermissionError("Teacher does not have access to this submission")

        # Create assessment
        assessment_id = Assessment.create_assessment(
            submission_id, teacher_id, grade, feedback
        )

        # Log action
        AccessLog.log_action(teacher_id, 'grade_submission',
                             'submission', submission_id)

        return assessment_id


class StudentService:
    """Student service"""

    @staticmethod
    def get_student_dashboard(student_id: int) -> Dict[str, Any]:
        """Get student dashboard data"""
        if not PermissionService.is_student(student_id):
            raise PermissionError("User is not a student")

        # Get student's classes
        enrolled_classes = ClassEnrollment.get_student_classes(student_id)

        # Get student's programs
        from models.program_models import ProgramEnrollment
        enrolled_programs = ProgramEnrollment.get_user_programs(student_id)

        # Get student's submissions and assessments
        from models.class_models import Submission
        submissions = Submission.get_student_submissions(student_id)
        assessments = Assessment.get_student_assessments(student_id)

        # Statistics
        dashboard = {
            'student_id': student_id,
            'total_classes': len(enrolled_classes),
            'total_programs': len(enrolled_programs),
            'total_submissions': len(submissions),
            'graded_submissions': len([s for s in submissions if s['status'] == 'graded']),
            'classes': enrolled_classes,
            'programs': enrolled_programs,
            'recent_assessments': assessments[:10]
        }

        return dashboard

    @staticmethod
    def submit_assignment(student_id: int, activity_id: int,
                          submission_data: Optional[str] = None,
                          submission_file_path: Optional[str] = None) -> int:
        """Student submits assignment"""
        from models.class_models import Activity, Submission

        # Validate if student has permission to submit
        activity = Activity.find_by_id(activity_id)
        if not activity or not activity['class_id']:
            raise ValueError("Invalid activity")

        # Check if student is enrolled in this class
        if not ClassEnrollment.check_enrollment(activity['class_id'], student_id):
            raise PermissionError("Student is not enrolled in this class")

        # Create submission
        submission_id = Submission.create_submission(
            activity_id, student_id, submission_data, submission_file_path
        )

        # Log action
        AccessLog.log_action(student_id, 'submit_assignment',
                             'activity', activity_id)

        return submission_id


class PrincipalService:
    """Principal service"""

    @staticmethod
    def get_school_dashboard(principal_id: int, org_id: int) -> Dict[str, Any]:
        """Get school dashboard data"""
        if not PermissionService.is_principal(principal_id, org_id):
            raise PermissionError("User is not a principal of this organization")

        # Get school information
        org = Organization.find_by_id(org_id)
        if not org or org['org_type'] != Organization.SCHOOL:
            raise ValueError("Invalid school organization")

        # Get school member statistics
        teachers = Organization.get_organization_members(org_id, 'teacher')
        students = Organization.get_organization_members(org_id, 'student')

        # Get school's classes
        classes = Organization.get_organization_classes(org_id)

        # Get school library content
        library_content = ContentLibrary.get_organization_library(org_id, include_private=True)

        dashboard = {
            'organization': org,
            'total_teachers': len(teachers),
            'total_students': len(students),
            'total_classes': len(classes),
            'total_library_items': len(library_content),
            'subscription_status': org['subscription_status'],
            'teachers': teachers,
            'students': students[:20],  # Latest 20 students
            'classes': classes
        }

        return dashboard

    @staticmethod
    def generate_student_access_code(principal_id: int, org_id: int,
                                     student_id: int) -> str:
        """Generate access code for student"""
        if not PermissionService.is_principal(principal_id, org_id):
            raise PermissionError("User is not a principal of this organization")

        # Verify student is in this organization
        role = OrganizationMember.get_member_role(org_id, student_id)
        if role != OrganizationMember.STUDENT:
            raise ValueError("User is not a student of this organization")

        # Generate access code
        access_code = OrganizationMember.generate_access_code(org_id, student_id)

        # Log action
        AccessLog.log_action(principal_id, 'generate_access_code',
                             'student', student_id)

        return access_code


class PublicService:
    """Public access service"""

    @staticmethod
    def get_public_content(content_type: Optional[str] = None,
                           limit: int = 100) -> List[Dict[str, Any]]:
        """Get public content (no authentication required)"""
        return ContentLibrary.get_public_content(content_type, limit)

    @staticmethod
    def get_community_library(community_id: int) -> Dict[str, Any]:
        """Get community library (public access)"""
        org = Organization.find_by_id(community_id)
        if not org or org['org_type'] != Organization.COMMUNITY:
            raise ValueError("Invalid community organization")

        if not org['is_public']:
            raise PermissionError("This community is not public")

        # Get community content
        content = ContentLibrary.get_organization_library(community_id, include_private=False)

        # Get community members (public profiles)
        from models.user_models import UserProfile
        members = Organization.get_organization_members(community_id)

        public_members = []
        for member in members:
            profile = UserProfile.get_by_user_id(member['user_id'])
            if profile and profile['is_public']:
                public_members.append({
                    'user_id': member['user_id'],
                    'username': member['username'],
                    'role': member['role'],
                    'profile': profile
                })

        return {
            'organization': org,
            'content': content,
            'members': public_members
        }

    @staticmethod
    def browse_species_sightings(species_name: Optional[str] = None,
                                 location: Optional[str] = None,
                                 verified_only: bool = True) -> List[Dict[str, Any]]:
        """Browse species sighting records (public access)"""
        if species_name:
            sightings = SpeciesSighting.get_species_sightings(species_name)
        elif location:
            sightings = SpeciesSighting.get_location_sightings(location)
        else:
            sightings = SpeciesSighting.get_all_sightings(verified_only=verified_only)

        return sightings
