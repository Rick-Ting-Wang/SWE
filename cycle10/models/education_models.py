"""
Education-related models for classes, programs, and activities
"""
from typing import Optional, List, Dict, Any
from models import BaseModel


class ClassModel(BaseModel):
    """Class model for course-related operations"""

    def create_class(self, org_id: int, teacher_id: int, class_name: str,
                    syllabus: Optional[str] = None) -> int:
        """Create a new class/course"""
        return self._execute_insert(
            """INSERT INTO classes (org_id, teacher_id, class_name, syllabus)
               VALUES (%s, %s, %s, %s)""",
            (org_id, teacher_id, class_name, syllabus)
        )

    def enroll_student(self, class_id: int, student_id: int) -> bool:
        """Enroll student in class"""
        try:
            self._execute_insert(
                """INSERT INTO class_enrollments (class_id, student_id, enrollment_date)
                   VALUES (%s, %s, CURDATE())""",
                (class_id, student_id)
            )
            return True
        except Exception:
            return False

    def get_available_classes(self) -> List[Dict[str, Any]]:
        """Get all available classes"""
        return self._execute_query(
            """SELECT c.class_id, c.class_name, o.org_name
               FROM classes c
               JOIN organizations o ON c.org_id = o.org_id"""
        )

    def get_teacher_classes(self, teacher_id: int) -> List[Dict[str, Any]]:
        """Get classes taught by teacher"""
        return self._execute_query(
            """SELECT class_id, class_name
               FROM classes
               WHERE teacher_id = %s""",
            (teacher_id,)
        )


class ProgramModel(BaseModel):
    """Program model for program-related operations"""

    def create_program(self, program_name: str, description: str,
                      program_type: str) -> int:
        """Create a new program"""
        return self._execute_insert(
            """INSERT INTO programs (program_name, description, program_type)
               VALUES (%s, %s, %s)""",
            (program_name, description, program_type)
        )

    def enroll_in_program(self, program_id: int, user_id: Optional[int],
                         org_id: Optional[int]) -> bool:
        """Enroll user or organization in program"""
        try:
            self._execute_insert(
                """INSERT INTO program_enrollments (program_id, user_id, org_id, enrollment_date)
                   VALUES (%s, %s, %s, CURDATE())""",
                (program_id, user_id, org_id)
            )
            return True
        except Exception:
            return False

    def get_available_programs(self) -> List[Dict[str, Any]]:
        """Get all available programs"""
        return self._execute_query(
            "SELECT program_id, program_name FROM programs"
        )


class ActivityModel(BaseModel):
    """Activity model for activity-related operations"""

    def create_activity(self, program_id: int, class_id: Optional[int],
                       activity_name: str, activity_type: str,
                       description: str, created_by: int) -> int:
        """Create a new activity"""
        return self._execute_insert(
            """INSERT INTO activities (program_id, class_id, activity_name,
                   activity_type, description, created_by)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (program_id, class_id, activity_name, activity_type, description, created_by)
        )

    def get_available_activities(self) -> List[Dict[str, Any]]:
        """Get all available activities"""
        return self._execute_query(
            """SELECT a.activity_id, a.activity_name, p.program_name
               FROM activities a
               JOIN programs p ON a.program_id = p.program_id"""
        )


class SubmissionModel(BaseModel):
    """Submission model for assignment submissions"""

    def submit_assignment(self, activity_id: int, student_id: int,
                         submission_data: str, submission_file_path: Optional[str] = None) -> int:
        """Submit assignment"""
        return self._execute_insert(
            """INSERT INTO submissions (activity_id, student_id, submission_data, submission_file_path)
               VALUES (%s, %s, %s, %s)""",
            (activity_id, student_id, submission_data, submission_file_path)
        )

    def get_pending_submissions(self, teacher_id: int) -> List[Dict[str, Any]]:
        """Get submissions pending grading"""
        return self._execute_query(
            """SELECT s.submission_id, s.activity_id, a.activity_name,
                      s.student_id, u.username, s.submission_data
               FROM submissions s
               JOIN activities a ON s.activity_id = a.activity_id
               JOIN users u ON s.student_id = u.user_id
               WHERE s.status != 'graded' AND a.created_by = %s""",
            (teacher_id,)
        )

    def grade_submission(self, submission_id: int, teacher_id: int,
                        grade: str, feedback: str) -> bool:
        """Grade submission"""
        try:
            # Create assessment
            self._execute_insert(
                """INSERT INTO assessments (submission_id, teacher_id, grade, feedback)
                   VALUES (%s, %s, %s, %s)""",
                (submission_id, teacher_id, grade, feedback)
            )

            # Update submission status
            self._execute_update(
                "UPDATE submissions SET status = 'graded' WHERE submission_id = %s",
                (submission_id,)
            )
            return True
        except Exception:
            return False