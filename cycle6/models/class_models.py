"""
Komodo Hub - Teaching and Class Models
Class, Activity, Submission, and Assessment models
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from database import BaseModel, db


class Class(BaseModel):
    """Class/Course model"""

    table_name = 'classes'
    primary_key = 'class_id'

    @classmethod
    def create_class(cls, org_id: int, teacher_id: int,
                     class_name: str, syllabus: Optional[str] = None) -> int:
        """Create a new class"""
        data = {
            'org_id': org_id,
            'teacher_id': teacher_id,
            'class_name': class_name
        }

        if syllabus:
            data['syllabus'] = syllabus

        return cls.insert(data)

    @classmethod
    def get_teacher_classes(cls, teacher_id: int) -> List[Dict[str, Any]]:
        """Get all classes taught by a teacher"""
        query = """
                SELECT c.*, o.org_name
                FROM classes c
                         JOIN organizations o ON c.org_id = o.org_id
                WHERE c.teacher_id = %s
                ORDER BY c.created_at DESC \
                """
        return db.execute_query(query, (teacher_id,))

    @classmethod
    def get_organization_classes(cls, org_id: int) -> List[Dict[str, Any]]:
        """Get all classes in an organization"""
        query = """
                SELECT c.*, u.username as teacher_name
                FROM classes c
                         JOIN users u ON c.teacher_id = u.user_id
                WHERE c.org_id = %s
                ORDER BY c.created_at DESC \
                """
        return db.execute_query(query, (org_id,))

    @classmethod
    def get_class_students(cls, class_id: int) -> List[Dict[str, Any]]:
        """Get all students in a class"""
        query = """
                SELECT u.*, ce.enrollment_date, ce.status
                FROM users u
                         JOIN class_enrollments ce ON u.user_id = ce.student_id
                WHERE ce.class_id = %s \
                  AND ce.status = 'active'
                ORDER BY u.username \
                """
        return db.execute_query(query, (class_id,))

    @classmethod
    def get_class_count_by_teacher(cls, teacher_id: int) -> int:
        """Get the number of classes taught by a teacher"""
        return cls.count({'teacher_id': teacher_id})


class ClassEnrollment(BaseModel):
    """Class enrollment model"""

    table_name = 'class_enrollments'
    primary_key = 'enrollment_id'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    @classmethod
    def enroll_student(cls, class_id: int, student_id: int,
                       enrollment_date: Optional[date] = None) -> int:
        """Enroll a student in a class"""
        data = {
            'class_id': class_id,
            'student_id': student_id,
            'enrollment_date': enrollment_date or date.today(),
            'status': cls.STATUS_ACTIVE
        }

        return cls.insert(data)

    @classmethod
    def get_student_classes(cls, student_id: int, status: str = STATUS_ACTIVE) -> List[Dict[str, Any]]:
        """Get all classes a student is enrolled in"""
        query = """
                SELECT c.*, u.username as teacher_name, ce.enrollment_date, ce.status
                FROM classes c
                         JOIN class_enrollments ce ON c.class_id = ce.class_id
                         JOIN users u ON c.teacher_id = u.user_id
                WHERE ce.student_id = %s \
                  AND ce.status = %s
                ORDER BY ce.enrollment_date DESC \
                """
        return db.execute_query(query, (student_id, status))

    @classmethod
    def update_status(cls, class_id: int, student_id: int, status: str) -> int:
        """Update enrollment status"""
        query = f"UPDATE {cls.table_name} SET status = %s WHERE class_id = %s AND student_id = %s"
        return db.execute_update(query, (status, class_id, student_id))

    @classmethod
    def check_enrollment(cls, class_id: int, student_id: int) -> bool:
        """Check if a student is enrolled in a class"""
        query = f"SELECT COUNT(*) as count FROM {cls.table_name} WHERE class_id = %s AND student_id = %s"
        result = db.execute_query(query, (class_id, student_id))
        return result[0]['count'] > 0 if result else False


class Activity(BaseModel):
    """Activity model"""

    table_name = 'activities'
    primary_key = 'activity_id'

    # Activity type constants
    IN_CLASS = 'in-class'
    OUTDOOR = 'outdoor'
    CHALLENGE = 'challenge'
    GAME = 'game'
    ASSESSMENT = 'assessment'

    @classmethod
    def create_activity(cls, program_id: int, activity_name: str,
                        activity_type: str, created_by: int,
                        class_id: Optional[int] = None,
                        description: Optional[str] = None) -> int:
        """Create a new activity"""
        data = {
            'program_id': program_id,
            'activity_name': activity_name,
            'activity_type': activity_type,
            'created_by': created_by
        }

        if class_id:
            data['class_id'] = class_id
        if description:
            data['description'] = description

        return cls.insert(data)

    @classmethod
    def get_class_activities(cls, class_id: int) -> List[Dict[str, Any]]:
        """Get all activities for a class"""
        query = """
                SELECT a.*, p.program_name, u.username as creator_name
                FROM activities a
                         JOIN programs p ON a.program_id = p.program_id
                         JOIN users u ON a.created_by = u.user_id
                WHERE a.class_id = %s
                ORDER BY a.created_at DESC \
                """
        return db.execute_query(query, (class_id,))

    @classmethod
    def get_program_activities(cls, program_id: int,
                               activity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all activities for a program"""
        if activity_type:
            query = """
                    SELECT a.*, u.username as creator_name
                    FROM activities a
                             JOIN users u ON a.created_by = u.user_id
                    WHERE a.program_id = %s \
                      AND a.activity_type = %s
                    ORDER BY a.created_at DESC \
                    """
            return db.execute_query(query, (program_id, activity_type))
        else:
            query = """
                    SELECT a.*, u.username as creator_name
                    FROM activities a
                             JOIN users u ON a.created_by = u.user_id
                    WHERE a.program_id = %s
                    ORDER BY a.created_at DESC \
                    """
            return db.execute_query(query, (program_id,))

    @classmethod
    def get_teacher_activities(cls, teacher_id: int) -> List[Dict[str, Any]]:
        """Get all activities created by a teacher"""
        query = """
                SELECT a.*, p.program_name, c.class_name
                FROM activities a
                         JOIN programs p ON a.program_id = p.program_id
                         LEFT JOIN classes c ON a.class_id = c.class_id
                WHERE a.created_by = %s
                ORDER BY a.created_at DESC \
                """
        return db.execute_query(query, (teacher_id,))


class Submission(BaseModel):
    """Submission model"""

    table_name = 'submissions'
    primary_key = 'submission_id'

    STATUS_SUBMITTED = 'submitted'
    STATUS_GRADED = 'graded'
    STATUS_RETURNED = 'returned'

    @classmethod
    def create_submission(cls, activity_id: int, student_id: int,
                          submission_data: Optional[str] = None,
                          submission_file_path: Optional[str] = None) -> int:
        """Create a new submission"""
        data = {
            'activity_id': activity_id,
            'student_id': student_id,
            'status': cls.STATUS_SUBMITTED
        }

        if submission_data:
            data['submission_data'] = submission_data
        if submission_file_path:
            data['submission_file_path'] = submission_file_path

        return cls.insert(data)

    @classmethod
    def get_activity_submissions(cls, activity_id: int) -> List[Dict[str, Any]]:
        """Get all submissions for an activity"""
        query = """
                SELECT s.*, u.username as student_name
                FROM submissions s
                         JOIN users u ON s.student_id = u.user_id
                WHERE s.activity_id = %s
                ORDER BY s.submission_date DESC \
                """
        return db.execute_query(query, (activity_id,))

    @classmethod
    def get_student_submissions(cls, student_id: int,
                                status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all submissions of a student"""
        if status:
            query = """
                    SELECT s.*, a.activity_name, a.activity_type
                    FROM submissions s
                             JOIN activities a ON s.activity_id = a.activity_id
                    WHERE s.student_id = %s \
                      AND s.status = %s
                    ORDER BY s.submission_date DESC \
                    """
            return db.execute_query(query, (student_id, status))
        else:
            query = """
                    SELECT s.*, a.activity_name, a.activity_type
                    FROM submissions s
                             JOIN activities a ON s.activity_id = a.activity_id
                    WHERE s.student_id = %s
                    ORDER BY s.submission_date DESC \
                    """
            return db.execute_query(query, (student_id,))

    @classmethod
    def get_teacher_class_submissions(cls, teacher_id: int) -> List[Dict[str, Any]]:
        """Get all submissions for all classes of a teacher"""
        query = """
                SELECT s.*, a.activity_name, u.username as student_name, c.class_name
                FROM submissions s
                         JOIN activities a ON s.activity_id = a.activity_id
                         JOIN users u ON s.student_id = u.user_id
                         JOIN classes c ON a.class_id = c.class_id
                WHERE c.teacher_id = %s
                ORDER BY s.submission_date DESC \
                """
        return db.execute_query(query, (teacher_id,))

    @classmethod
    def update_status(cls, submission_id: int, status: str) -> int:
        """Update submission status"""
        return cls.update(submission_id, {'status': status})


class Assessment(BaseModel):
    """Assessment/Grading model"""

    table_name = 'assessments'
    primary_key = 'assessment_id'

    @classmethod
    def create_assessment(cls, submission_id: int, teacher_id: int,
                          grade: Optional[str] = None,
                          feedback: Optional[str] = None) -> int:
        """Create a new assessment"""
        data = {
            'submission_id': submission_id,
            'teacher_id': teacher_id
        }

        if grade:
            data['grade'] = grade
        if feedback:
            data['feedback'] = feedback

        # Update submission status after creating assessment
        assessment_id = cls.insert(data)
        Submission.update_status(submission_id, Submission.STATUS_GRADED)

        return assessment_id

    @classmethod
    def get_submission_assessment(cls, submission_id: int) -> Optional[Dict[str, Any]]:
        """Get the assessment for a submission"""
        query = """
                SELECT a.*, u.username as teacher_name
                FROM assessments a
                         JOIN users u ON a.teacher_id = u.user_id
                WHERE a.submission_id = %s \
                """
        results = db.execute_query(query, (submission_id,))
        return results[0] if results else None

    @classmethod
    def get_student_assessments(cls, student_id: int) -> List[Dict[str, Any]]:
        """Get all assessments for a student"""
        query = """
                SELECT a.*, s.activity_id, act.activity_name, u.username as teacher_name
                FROM assessments a
                         JOIN submissions s ON a.submission_id = s.submission_id
                         JOIN activities act ON s.activity_id = act.activity_id
                         JOIN users u ON a.teacher_id = u.user_id
                WHERE s.student_id = %s
                ORDER BY a.assessed_at DESC \
                """
        return db.execute_query(query, (student_id,))

    @classmethod
    def get_teacher_assessments(cls, teacher_id: int) -> List[Dict[str, Any]]:
        """Get all assessments made by a teacher"""
        query = """
                SELECT a.*, \
                       s.student_id, \
                       u.username as student_name,
                       act.activity_name
                FROM assessments a
                         JOIN submissions s ON a.submission_id = s.submission_id
                         JOIN users u ON s.student_id = u.user_id
                         JOIN activities act ON s.activity_id = act.activity_id
                WHERE a.teacher_id = %s
                ORDER BY a.assessed_at DESC \
                """
        return db.execute_query(query, (teacher_id,))

    @classmethod
    def update_assessment(cls, assessment_id: int,
                          grade: Optional[str] = None,
                          feedback: Optional[str] = None) -> int:
        """Update assessment"""
        data = {}
        if grade is not None:
            data['grade'] = grade
        if feedback is not None:
            data['feedback'] = feedback

        return cls.update(assessment_id, data)

    @classmethod
    def get_student_progress_report(cls, student_id: int, class_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Generate a student progress report"""
        if class_id:
            query = """
                    SELECT c.class_name, \
                           a.activity_name, \
                           a.activity_type, \
                           s.submission_date, \
                           ass.grade, \
                           ass.feedback, \
                           ass.assessed_at
                    FROM assessments ass
                             JOIN submissions s ON ass.submission_id = s.submission_id
                             JOIN activities a ON s.activity_id = a.activity_id
                             JOIN classes c ON a.class_id = c.class_id
                    WHERE s.student_id = %s \
                      AND c.class_id = %s
                    ORDER BY ass.assessed_at DESC \
                    """
            return db.execute_query(query, (student_id, class_id))
        else:
            query = """
                    SELECT c.class_name, \
                           a.activity_name, \
                           a.activity_type, \
                           s.submission_date, \
                           ass.grade, \
                           ass.feedback, \
                           ass.assessed_at
                    FROM assessments ass
                             JOIN submissions s ON ass.submission_id = s.submission_id
                             JOIN activities a ON s.activity_id = a.activity_id
                             JOIN classes c ON a.class_id = c.class_id
                    WHERE s.student_id = %s
                    ORDER BY ass.assessed_at DESC \
                    """
            return db.execute_query(query, (student_id,))
