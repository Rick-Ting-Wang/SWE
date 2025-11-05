"""
Database models tests
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pymysql
from models import DatabaseManager, BaseModel
from models.user_models import UserModel, OrganizationModel, MessageModel
from models.education_models import ClassModel, ProgramModel, ActivityModel, SubmissionModel
from models.content_models import ContentModel, SightingModel, AnalyticsModel, CanvasModel


class TestDatabaseManager(unittest.TestCase):
    """Test DatabaseManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_config = Mock()
        self.mock_config.DB_HOST = 'localhost'
        self.mock_config.DB_PORT = 3306
        self.mock_config.DB_NAME = 'test_db'
        self.mock_config.DB_USER = 'test_user'
        self.mock_config.DB_PASSWORD = 'test_pass'

    @patch('models.pymysql.connect')
    def test_get_connection(self, mock_connect):
        """Test database connection"""
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        db_manager = DatabaseManager(self.mock_config)
        connection = db_manager.get_connection()

        # Verify connection was created with correct parameters
        mock_connect.assert_called_once_with(
            host='localhost',
            port=3306,
            user='test_user',
            password='test_pass',
            database='test_db',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.assertEqual(connection, mock_conn)

    @patch('models.pymysql.connect')
    def test_cursor_context_manager(self, mock_connect):
        """Test cursor context manager"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_manager = DatabaseManager(self.mock_config)
        with db_manager.cursor() as cursor:
            self.assertEqual(cursor, mock_cursor)

        # Verify cursor was closed
        mock_cursor.close.assert_called_once()

    @patch('models.pymysql.connect')
    def test_execute_query(self, mock_connect):
        """Test query execution"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'test'}]

        db_manager = DatabaseManager(self.mock_config)
        result = db_manager.execute_query("SELECT * FROM test", ())

        # Verify query was executed
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test", ())
        self.assertEqual(result, [{'id': 1, 'name': 'test'}])


class TestBaseModel(unittest.TestCase):
    """Test BaseModel class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.base_model = BaseModel(self.mock_db_manager)

    def test_init(self):
        """Test BaseModel initialization"""
        self.assertEqual(self.base_model.db, self.mock_db_manager)

    def test_execute_query(self):
        """Test _execute_query method"""
        expected_result = [{'id': 1}]
        self.mock_db_manager.execute_query.return_value = expected_result

        result = self.base_model._execute_query("SELECT * FROM test", (1,))

        self.mock_db_manager.execute_query.assert_called_once_with("SELECT * FROM test", (1,))
        self.assertEqual(result, expected_result)

    def test_execute_update(self):
        """Test _execute_update method"""
        self.mock_db_manager.execute_update.return_value = 1

        result = self.base_model._execute_update("UPDATE test SET name=%s", ('new_name',))

        self.mock_db_manager.execute_update.assert_called_once_with("UPDATE test SET name=%s", ('new_name',))
        self.assertEqual(result, 1)

    def test_execute_insert(self):
        """Test _execute_insert method"""
        self.mock_db_manager.execute_insert.return_value = 123

        result = self.base_model._execute_insert("INSERT INTO test (name) VALUES (%s)", ('test',))

        self.mock_db_manager.execute_insert.assert_called_once_with("INSERT INTO test (name) VALUES (%s)", ('test',))
        self.assertEqual(result, 123)


class TestUserModels(unittest.TestCase):
    """Test user-related models"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.user_model = UserModel(self.mock_db_manager)
        self.org_model = OrganizationModel(self.mock_db_manager)
        self.message_model = MessageModel(self.mock_db_manager)

    def test_get_user_by_id(self):
        """Test get_user_by_id method"""
        expected_user = {'user_id': 1, 'username': 'test_user'}
        self.mock_db_manager.execute_query.return_value = [expected_user]

        result = self.user_model.get_user_by_id(1)

        self.mock_db_manager.execute_query.assert_called_once_with(
            "SELECT * FROM users WHERE user_id = %s", (1,)
        )
        self.assertEqual(result, expected_user)

    def test_get_user_by_id_not_found(self):
        """Test get_user_by_id when user not found"""
        self.mock_db_manager.execute_query.return_value = []

        result = self.user_model.get_user_by_id(999)

        self.assertIsNone(result)

    def test_create_user(self):
        """Test create_user method"""
        self.mock_db_manager.execute_insert.side_effect = [123, 1]

        user_id = self.user_model.create_user(
            'test_user', 'test@example.com', 'hashed_password', 'student'
        )

        # Verify user creation
        self.mock_db_manager.execute_insert.assert_any_call(
            """INSERT INTO users (user_image, username, email, password, user_type)
               VALUES (%s, %s, %s, %s, %s)""",
            ('1', 'test_user', 'test@example.com', 'hashed_password', 'student')
        )

        # Verify profile creation
        self.mock_db_manager.execute_insert.assert_any_call(
            "INSERT INTO user_profiles (user_id) VALUES (%s)", (123,)
        )

        self.assertEqual(user_id, 123)

    def test_send_message(self):
        """Test send_message method"""
        self.mock_db_manager.execute_insert.return_value = 456

        message_id = self.message_model.send_message(1, 2, "Hello!")

        self.mock_db_manager.execute_insert.assert_called_once_with(
            """INSERT INTO messages (sender_id, recipient_id, message_text)
               VALUES (%s, %s, %s)""",
            (1, 2, "Hello!")
        )
        self.assertEqual(message_id, 456)


class TestEducationModels(unittest.TestCase):
    """Test education-related models"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.class_model = ClassModel(self.mock_db_manager)
        self.program_model = ProgramModel(self.mock_db_manager)
        self.activity_model = ActivityModel(self.mock_db_manager)
        self.submission_model = SubmissionModel(self.mock_db_manager)

    def test_create_class(self):
        """Test create_class method"""
        self.mock_db_manager.execute_insert.return_value = 100

        class_id = self.class_model.create_class(1, 2, "Math Class", "Math syllabus")

        self.mock_db_manager.execute_insert.assert_called_once_with(
            """INSERT INTO classes (org_id, teacher_id, class_name, syllabus)
               VALUES (%s, %s, %s, %s)""",
            (1, 2, "Math Class", "Math syllabus")
        )
        self.assertEqual(class_id, 100)

    def test_enroll_student_success(self):
        """Test successful student enrollment"""
        self.mock_db_manager.execute_insert.return_value = 1

        result = self.class_model.enroll_student(1, 2)

        self.mock_db_manager.execute_insert.assert_called_once_with(
            """INSERT INTO class_enrollments (class_id, student_id, enrollment_date)
               VALUES (%s, %s, CURDATE())""",
            (1, 2)
        )
        self.assertTrue(result)

    def test_enroll_student_failure(self):
        """Test failed student enrollment"""
        self.mock_db_manager.execute_insert.side_effect = Exception("Duplicate entry")

        result = self.class_model.enroll_student(1, 2)

        self.assertFalse(result)

    def test_create_program(self):
        """Test create_program method"""
        self.mock_db_manager.execute_insert.return_value = 200

        program_id = self.program_model.create_program(
            "Conservation Program", "Program description", "regional"
        )

        self.mock_db_manager.execute_insert.assert_called_once_with(
            """INSERT INTO programs (program_name, description, program_type)
               VALUES (%s, %s, %s)""",
            ("Conservation Program", "Program description", "regional")
        )
        self.assertEqual(program_id, 200)


class TestContentModels(unittest.TestCase):
    """Test content-related models"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_manager = Mock()
        self.content_model = ContentModel(self.mock_db_manager)
        self.sighting_model = SightingModel(self.mock_db_manager)
        self.analytics_model = AnalyticsModel(self.mock_db_manager)
        self.canvas_model = CanvasModel(self.mock_db_manager)

    def test_upload_content(self):
        """Test upload_content method"""
        self.mock_db_manager.execute_insert.return_value = 300

        content_id = self.content_model.upload_content(
            "Test Article", "article", "Content data", 1, 1, True
        )

        self.mock_db_manager.execute_insert.assert_called_once_with(
            """INSERT INTO content_library (title, content_type, content_data,
                   created_by, org_id, is_public)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            ("Test Article", "article", "Content data", 1, 1, True)
        )
        self.assertEqual(content_id, 300)

    def test_report_sighting(self):
        """Test report_sighting method"""
        self.mock_db_manager.execute_insert.return_value = 400

        sighting_id = self.sighting_model.report_sighting(
            "Komodo Dragon", "Indonesia", "2024-01-01 10:00:00",
            "Large specimen", "photo.jpg", 1
        )

        self.mock_db_manager.execute_insert.assert_called_once_with(
            """INSERT INTO species_sightings (species_name, location, date_time,
                   description, photo_path, reported_by)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            ("Komodo Dragon", "Indonesia", "2024-01-01 10:00:00",
             "Large specimen", "photo.jpg", 1)
        )
        self.assertEqual(sighting_id, 400)

    def test_save_canvas_success(self):
        """Test successful canvas save"""
        self.mock_db_manager.execute_insert.return_value = 1

        result = self.canvas_model.save_canvas(1, 1, '{"assets": []}')

        self.mock_db_manager.execute_insert.assert_called_once_with(
            """INSERT INTO creative_canvas (user_id, program_id, assets)
               VALUES (%s, %s, %s) ON DUPLICATE KEY
               UPDATE assets = %s, updated_at = NOW()""",
            (1, 1, '{"assets": []}', '{"assets": []}')
        )
        self.assertTrue(result)

    def test_save_canvas_failure(self):
        """Test failed canvas save"""
        self.mock_db_manager.execute_insert.side_effect = Exception("Database error")

        result = self.canvas_model.save_canvas(1, 1, '{"assets": []}')

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()