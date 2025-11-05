"""
Services layer tests
"""
import unittest
from unittest.mock import Mock, patch
import hashlib
from services import AuthService, UserService, OrganizationService, EducationService, ContentService


class TestAuthService(unittest.TestCase):
    """Test AuthService class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.auth_service = AuthService(self.mock_db_manager)

    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password"
        expected_hash = hashlib.sha256(password.encode()).hexdigest()

        result = self.auth_service.hash_password(password)

        self.assertEqual(result, expected_hash)

    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        email = "test@example.com"
        password = "password123"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        mock_user = {
            'user_id': 1,
            'username': 'test_user',
            'email': email,
            'password': hashed_password,
            'user_type': 'student'
        }

        # Mock the user model
        self.auth_service.user_model.get_user_by_email.return_value = mock_user
        self.auth_service.user_model.update_last_login.return_value = None

        result = self.auth_service.authenticate_user(email, password)

        # Verify user lookup
        self.auth_service.user_model.get_user_by_email.assert_called_once_with(email)
        # Verify last login update
        self.auth_service.user_model.update_last_login.assert_called_once_with(1)
        # Verify returned user
        self.assertEqual(result, mock_user)

    def test_authenticate_user_failure_wrong_password(self):
        """Test authentication failure with wrong password"""
        email = "test@example.com"
        password = "wrong_password"
        hashed_password = hashlib.sha256("correct_password".encode()).hexdigest()

        mock_user = {
            'user_id': 1,
            'username': 'test_user',
            'email': email,
            'password': hashed_password,
            'user_type': 'student'
        }

        self.auth_service.user_model.get_user_by_email.return_value = mock_user

        result = self.auth_service.authenticate_user(email, password)

        self.assertIsNone(result)
        self.auth_service.user_model.update_last_login.assert_not_called()

    def test_authenticate_user_failure_user_not_found(self):
        """Test authentication failure when user not found"""
        self.auth_service.user_model.get_user_by_email.return_value = None

        result = self.auth_service.authenticate_user("nonexistent@example.com", "password")

        self.assertIsNone(result)

    def test_register_user_success(self):
        """Test successful user registration"""
        username = "new_user"
        email = "new@example.com"
        password = "password123"
        user_type = "student"

        self.auth_service.user_model.create_user.return_value = 123

        user_id = self.auth_service.register_user(username, email, password, user_type)

        # Verify user creation with hashed password
        expected_hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.auth_service.user_model.create_user.assert_called_once_with(
            username, email, expected_hashed_password, user_type, '1'
        )
        self.assertEqual(user_id, 123)

    def test_register_user_failure(self):
        """Test failed user registration"""
        self.auth_service.user_model.create_user.side_effect = Exception("Duplicate email")

        user_id = self.auth_service.register_user("user", "email@example.com", "pass", "student")

        self.assertIsNone(user_id)


class TestUserService(unittest.TestCase):
    """Test UserService class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.user_service = UserService(self.mock_db_manager)

    def test_get_user_profile(self):
        """Test get_user_profile method"""
        mock_profile = {
            'user_id': 1,
            'username': 'test_user',
            'email': 'test@example.com',
            'user_type': 'student',
            'user_image': '2'
        }

        self.user_service.user_model.get_user_profile.return_value = mock_profile

        result = self.user_service.get_user_profile(1)

        # Verify profile retrieval
        self.user_service.user_model.get_user_profile.assert_called_once_with(1)
        # Verify avatar URL is added
        self.assertEqual(result['avatar_url'], "/static/avatar/2.jpg")

    def test_get_user_profile_not_found(self):
        """Test get_user_profile when user not found"""
        self.user_service.user_model.get_user_profile.return_value = {}

        result = self.user_service.get_user_profile(999)

        self.assertEqual(result, {})

    def test_get_received_messages(self):
        """Test get_received_messages method"""
        mock_messages = [
            {
                'message_id': 1,
                'message_text': 'Hello!',
                'sender_name': 'sender_user',
                'sender_id': 2
            }
        ]

        self.user_service.message_model.get_received_messages.return_value = mock_messages

        result = self.user_service.get_received_messages(1)

        self.user_service.message_model.get_received_messages.assert_called_once_with(1)
        self.assertEqual(result, mock_messages)

    def test_send_message_success(self):
        """Test successful message sending"""
        self.user_service.message_model.send_message.return_value = 456

        result = self.user_service.send_message(1, 2, "Test message")

        self.user_service.message_model.send_message.assert_called_once_with(1, 2, "Test message")
        self.assertTrue(result)

    def test_send_message_failure(self):
        """Test failed message sending"""
        self.user_service.message_model.send_message.side_effect = Exception("Database error")

        result = self.user_service.send_message(1, 2, "Test message")

        self.assertFalse(result)


class TestOrganizationService(unittest.TestCase):
    """Test OrganizationService class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.org_service = OrganizationService(self.mock_db_manager)

    def test_create_organization_success(self):
        """Test successful organization creation"""
        self.org_service.org_model.create_organization.return_value = 100
        self.org_service.org_model.add_organization_member.return_value = True

        org_id = self.org_service.create_organization(
            'school', 'Test School', 'School profile', True, 1
        )

        # Verify organization creation
        self.org_service.org_model.create_organization.assert_called_once_with(
            'school', 'Test School', 'School profile', True
        )
        # Verify member addition
        self.org_service.org_model.add_organization_member.assert_called_once_with(
            100, 1, 'admin'
        )
        self.assertEqual(org_id, 100)

    def test_create_organization_failure(self):
        """Test failed organization creation"""
        self.org_service.org_model.create_organization.side_effect = Exception("Database error")

        org_id = self.org_service.create_organization(
            'school', 'Test School', 'School profile', True, 1
        )

        self.assertIsNone(org_id)

    def test_join_organization_success_public(self):
        """Test successful join to public organization"""
        mock_org = {
            'org_id': 1,
            'org_type': 'school',
            'is_public': True
        }

        self.org_service.org_model._execute_query.return_value = [mock_org]
        self.org_service.org_model.add_organization_member.return_value = True

        result = self.org_service.join_organization(1, 2)

        # Verify organization lookup
        self.org_service.org_model._execute_query.assert_called_once_with(
            "SELECT * FROM organizations WHERE org_id = %s", (1,)
        )
        # Verify member addition with student role
        self.org_service.org_model.add_organization_member.assert_called_once_with(
            1, 2, 'student', None
        )
        self.assertTrue(result)

    def test_join_organization_private_without_code(self):
        """Test join private organization without access code"""
        mock_org = {
            'org_id': 1,
            'org_type': 'school',
            'is_public': False
        }

        self.org_service.org_model._execute_query.return_value = [mock_org]

        result = self.org_service.join_organization(1, 2)

        self.assertFalse(result)
        self.org_service.org_model.add_organization_member.assert_not_called()


class TestEducationService(unittest.TestCase):
    """Test EducationService class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.education_service = EducationService(self.mock_db_manager)

    def test_create_class_success(self):
        """Test successful class creation"""
        self.education_service.class_model.create_class.return_value = 200

        class_id = self.education_service.create_class(1, 2, "Math Class", "Syllabus")

        self.education_service.class_model.create_class.assert_called_once_with(
            1, 2, "Math Class", "Syllabus"
        )
        self.assertEqual(class_id, 200)

    def test_create_class_failure(self):
        """Test failed class creation"""
        self.education_service.class_model.create_class.side_effect = Exception("Database error")

        class_id = self.education_service.create_class(1, 2, "Math Class", "Syllabus")

        self.assertIsNone(class_id)

    def test_enroll_in_class_success(self):
        """Test successful class enrollment"""
        self.education_service.class_model.enroll_student.return_value = True

        result = self.education_service.enroll_in_class(1, 2)

        self.education_service.class_model.enroll_student.assert_called_once_with(1, 2)
        self.assertTrue(result)

    def test_create_program_success(self):
        """Test successful program creation"""
        self.education_service.program_model.create_program.return_value = 300

        program_id = self.education_service.create_program(
            "Conservation Program", "Program description", "regional"
        )

        self.education_service.program_model.create_program.assert_called_once_with(
            "Conservation Program", "Program description", "regional"
        )
        self.assertEqual(program_id, 300)

    def test_submit_assignment_success(self):
        """Test successful assignment submission"""
        self.education_service.submission_model.submit_assignment.return_value = 400

        submission_id = self.education_service.submit_assignment(
            1, 2, "Submission data", "file_path.jpg"
        )

        self.education_service.submission_model.submit_assignment.assert_called_once_with(
            1, 2, "Submission data", "file_path.jpg"
        )
        self.assertEqual(submission_id, 400)

    def test_grade_submission_success(self):
        """Test successful submission grading"""
        self.education_service.submission_model.grade_submission.return_value = True

        result = self.education_service.grade_submission(1, 2, "A", "Good work!")

        self.education_service.submission_model.grade_submission.assert_called_once_with(
            1, 2, "A", "Good work!"
        )
        self.assertTrue(result)


class TestContentService(unittest.TestCase):
    """Test ContentService class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.content_service = ContentService(self.mock_db_manager)

    def test_upload_content_success(self):
        """Test successful content upload"""
        self.content_service.content_model.upload_content.return_value = 500

        content_id = self.content_service.upload_content(
            "Test Article", "article", "Content data", 1, 1, True
        )

        self.content_service.content_model.upload_content.assert_called_once_with(
            "Test Article", "article", "Content data", 1, 1, True
        )
        self.assertEqual(content_id, 500)

    def test_report_sighting_success(self):
        """Test successful sighting report"""
        self.content_service.sighting_model.report_sighting.return_value = 600

        sighting_id = self.content_service.report_sighting(
            "Komodo Dragon", "Indonesia", "2024-01-01 10:00:00",
            "Large specimen", "photo.jpg", 1
        )

        self.content_service.sighting_model.report_sighting.assert_called_once_with(
            "Komodo Dragon", "Indonesia", "2024-01-01 10:00:00",
            "Large specimen", "photo.jpg", 1
        )
        self.assertEqual(sighting_id, 600)

    def test_save_canvas_success(self):
        """Test successful canvas save"""
        self.content_service.canvas_model.save_canvas.return_value = True

        result = self.content_service.save_canvas(1, 1, '{"assets": []}')

        self.content_service.canvas_model.save_canvas.assert_called_once_with(1, 1, '{"assets": []}')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()