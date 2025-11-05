"""
Komodo Hub - Program and Content Models
Program, Content Library, Species Sighting models
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from database import BaseModel, db


class Program(BaseModel):
    """Program/Conservation Plan model"""

    table_name = 'programs'
    primary_key = 'program_id'

    # Program type constants
    INTERNAL = 'internal'
    LOCAL = 'local'
    REGIONAL = 'regional'
    NATIONAL = 'national'

    @classmethod
    def create_program(cls, program_name: str, program_type: str,
                       description: Optional[str] = None) -> int:
        """Create new program"""
        data = {
            'program_name': program_name,
            'program_type': program_type
        }

        if description:
            data['description'] = description

        return cls.insert(data)

    @classmethod
    def get_by_type(cls, program_type: str) -> List[Dict[str, Any]]:
        """Get programs by type"""
        return cls.find_by_condition({'program_type': program_type}, limit=1000)

    @classmethod
    def get_popular_programs(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Get popular programs (by enrollment count)"""
        query = """
                SELECT p.*, \
                       COUNT(pe.enrollment_id) as enrollment_count
                FROM programs p
                         LEFT JOIN program_enrollments pe ON p.program_id = pe.program_id
                WHERE pe.status = 'active'
                GROUP BY p.program_id
                ORDER BY enrollment_count DESC
                    LIMIT %s \
                """
        return db.execute_query(query, (limit,))

    @classmethod
    def get_program_participants(cls, program_id: int) -> Dict[str, Any]:
        """Get participant statistics of a program"""
        query = """
                SELECT COUNT(DISTINCT pe.user_id) as individual_count, \
                       COUNT(DISTINCT pe.org_id)  as organization_count, \
                       COUNT(*)                   as total_enrollments
                FROM program_enrollments pe
                WHERE pe.program_id = %s \
                  AND pe.status = 'active' \
                """
        result = db.execute_query(query, (program_id,))
        return result[0] if result else {'individual_count': 0, 'organization_count': 0, 'total_enrollments': 0}


class ProgramEnrollment(BaseModel):
    """Program enrollment model"""

    table_name = 'program_enrollments'
    primary_key = 'enrollment_id'

    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_DROPPED = 'dropped'

    @classmethod
    def enroll_user(cls, program_id: int, user_id: int,
                    enrollment_date: Optional[date] = None) -> int:
        """User enrolls in program"""
        data = {
            'program_id': program_id,
            'user_id': user_id,
            'enrollment_date': enrollment_date or date.today(),
            'status': cls.STATUS_ACTIVE
        }

        return cls.insert(data)

    @classmethod
    def enroll_organization(cls, program_id: int, org_id: int,
                            enrollment_date: Optional[date] = None) -> int:
        """Organization enrolls in program"""
        data = {
            'program_id': program_id,
            'org_id': org_id,
            'enrollment_date': enrollment_date or date.today(),
            'status': cls.STATUS_ACTIVE
        }

        return cls.insert(data)

    @classmethod
    def get_user_programs(cls, user_id: int, status: str = STATUS_ACTIVE) -> List[Dict[str, Any]]:
        """Get programs user enrolled"""
        query = """
                SELECT p.*, pe.enrollment_date, pe.status
                FROM programs p
                         JOIN program_enrollments pe ON p.program_id = pe.program_id
                WHERE pe.user_id = %s \
                  AND pe.status = %s
                ORDER BY pe.enrollment_date DESC \
                """
        return db.execute_query(query, (user_id, status))

    @classmethod
    def get_organization_programs(cls, org_id: int, status: str = STATUS_ACTIVE) -> List[Dict[str, Any]]:
        """Get programs organization enrolled"""
        query = """
                SELECT p.*, pe.enrollment_date, pe.status
                FROM programs p
                         JOIN program_enrollments pe ON p.program_id = pe.program_id
                WHERE pe.org_id = %s \
                  AND pe.status = %s
                ORDER BY pe.enrollment_date DESC \
                """
        return db.execute_query(query, (org_id, status))

    @classmethod
    def update_status(cls, enrollment_id: int, status: str) -> int:
        """Update enrollment status"""
        return cls.update(enrollment_id, {'status': status})


class ContentLibrary(BaseModel):
    """Content library model"""

    table_name = 'content_library'
    primary_key = 'content_id'

    # Content type constants
    ARTICLE = 'article'
    ESSAY = 'essay'
    REPORT = 'report'
    SIGHTING = 'sighting'
    PHOTO = 'photo'
    VIDEO = 'video'
    EDUCATIONAL_MATERIAL = 'educational_material'

    @classmethod
    def create_content(cls, title: str, content_type: str, created_by: int,
                       content_data: Optional[str] = None,
                       org_id: Optional[int] = None,
                       is_public: bool = False) -> int:
        """Create new content"""
        data = {
            'title': title,
            'content_type': content_type,
            'created_by': created_by,
            'is_public': is_public
        }

        if content_data:
            data['content_data'] = content_data
        if org_id:
            data['org_id'] = org_id

        return cls.insert(data)

    @classmethod
    def get_public_content(cls, content_type: Optional[str] = None,
                           limit: int = 100) -> List[Dict[str, Any]]:
        """Get public content"""
        if content_type:
            query = """
                    SELECT cl.*, u.username as author_name
                    FROM content_library cl
                             JOIN users u ON cl.created_by = u.user_id
                    WHERE cl.is_public = TRUE \
                      AND cl.content_type = %s
                    ORDER BY cl.created_at DESC
                        LIMIT %s \
                    """
            return db.execute_query(query, (content_type, limit))
        else:
            query = """
                    SELECT cl.*, u.username as author_name
                    FROM content_library cl
                             JOIN users u ON cl.created_by = u.user_id
                    WHERE cl.is_public = TRUE
                    ORDER BY cl.created_at DESC
                        LIMIT %s \
                    """
            return db.execute_query(query, (limit,))

    @classmethod
    def get_organization_library(cls, org_id: int,
                                 include_private: bool = False) -> List[Dict[str, Any]]:
        """Get organization library content"""
        if include_private:
            query = """
                    SELECT cl.*, u.username as author_name
                    FROM content_library cl
                             JOIN users u ON cl.created_by = u.user_id
                    WHERE cl.org_id = %s
                    ORDER BY cl.created_at DESC \
                    """
        else:
            query = """
                    SELECT cl.*, u.username as author_name
                    FROM content_library cl
                             JOIN users u ON cl.created_by = u.user_id
                    WHERE cl.org_id = %s \
                      AND cl.is_public = TRUE
                    ORDER BY cl.created_at DESC \
                    """

        return db.execute_query(query, (org_id,))

    @classmethod
    def get_user_content(cls, user_id: int) -> List[Dict[str, Any]]:
        """Get content created by user"""
        query = """
                SELECT cl.*,
                       CASE WHEN cl.org_id IS NOT NULL THEN o.org_name ELSE NULL END as org_name
                FROM content_library cl
                         LEFT JOIN organizations o ON cl.org_id = o.org_id
                WHERE cl.created_by = %s
                ORDER BY cl.created_at DESC \
                """
        return db.execute_query(query, (user_id,))

    @classmethod
    def update_visibility(cls, content_id: int, is_public: bool) -> int:
        """Update content visibility"""
        return cls.update(content_id, {'is_public': is_public})

    @classmethod
    def search_content(cls, keyword: str, is_public_only: bool = True,
                       limit: int = 100) -> List[Dict[str, Any]]:
        """Search content"""
        keyword_pattern = f"%{keyword}%"

        if is_public_only:
            query = """
                    SELECT cl.*, u.username as author_name
                    FROM content_library cl
                             JOIN users u ON cl.created_by = u.user_id
                    WHERE cl.is_public = TRUE
                      AND (cl.title LIKE %s OR cl.content_data LIKE %s)
                    ORDER BY cl.created_at DESC
                        LIMIT %s \
                    """
        else:
            query = """
                    SELECT cl.*, u.username as author_name
                    FROM content_library cl
                             JOIN users u ON cl.created_by = u.user_id
                    WHERE cl.title LIKE %s \
                       OR cl.content_data LIKE %s
                    ORDER BY cl.created_at DESC
                        LIMIT %s \
                    """

        return db.execute_query(query, (keyword_pattern, keyword_pattern, limit))


class SpeciesSighting(BaseModel):
    """Species Sighting/Observation model"""

    table_name = 'species_sightings'
    primary_key = 'sighting_id'

    @classmethod
    def create_sighting(cls, species_name: str, location: str,
                        date_time: datetime, reported_by: int,
                        description: Optional[str] = None,
                        photo_path: Optional[str] = None) -> int:
        """Create species sighting record"""
        data = {
            'species_name': species_name,
            'location': location,
            'date_time': date_time,
            'reported_by': reported_by,
            'verified': False
        }

        if description:
            data['description'] = description
        if photo_path:
            data['photo_path'] = photo_path

        return cls.insert(data)

    @classmethod
    def verify_sighting(cls, sighting_id: int) -> int:
        """Verify species sighting record"""
        return cls.update(sighting_id, {'verified': True})

    @classmethod
    def get_all_sightings(cls, verified_only: bool = False,
                          limit: int = 100) -> List[Dict[str, Any]]:
        """Get all sighting records"""
        if verified_only:
            query = """
                    SELECT ss.*, u.username as reporter_name
                    FROM species_sightings ss
                             JOIN users u ON ss.reported_by = u.user_id
                    WHERE ss.verified = TRUE
                    ORDER BY ss.date_time DESC
                        LIMIT %s \
                    """
        else:
            query = """
                    SELECT ss.*, u.username as reporter_name
                    FROM species_sightings ss
                             JOIN users u ON ss.reported_by = u.user_id
                    ORDER BY ss.date_time DESC
                        LIMIT %s \
                    """

        return db.execute_query(query, (limit,))

    @classmethod
    def get_user_sightings(cls, user_id: int) -> List[Dict[str, Any]]:
        """Get user's sightings"""
        query = f"SELECT * FROM {cls.table_name} WHERE reported_by = %s ORDER BY date_time DESC"
        return db.execute_query(query, (user_id,))

    @classmethod
    def get_species_sightings(cls, species_name: str) -> List[Dict[str, Any]]:
        """Get sightings for a specific species"""
        query = """
                SELECT ss.*, u.username as reporter_name
                FROM species_sightings ss
                         JOIN users u ON ss.reported_by = u.user_id
                WHERE ss.species_name = %s
                ORDER BY ss.date_time DESC \
                """
        return db.execute_query(query, (species_name,))

    @classmethod
    def get_location_sightings(cls, location: str) -> List[Dict[str, Any]]:
        """Get sightings for a specific location"""
        location_pattern = f"%{location}%"
        query = """
                SELECT ss.*, u.username as reporter_name
                FROM species_sightings ss
                         JOIN users u ON ss.reported_by = u.user_id
                WHERE ss.location LIKE %s
                ORDER BY ss.date_time DESC \
                """
        return db.execute_query(query, (location_pattern,))

    @classmethod
    def get_sighting_statistics(cls) -> Dict[str, Any]:
        """Get sighting statistics"""
        query = """
                SELECT COUNT(*)                                         as total_sightings, \
                       COUNT(DISTINCT species_name)                     as unique_species, \
                       COUNT(DISTINCT reported_by)                      as unique_reporters, \
                       SUM(CASE WHEN verified = TRUE THEN 1 ELSE 0 END) as verified_count
                FROM species_sightings \
                """
        result = db.execute_query(query)
        return result[0] if result else {}


class CreativeCanvas(BaseModel):
    """Creative canvas model"""

    table_name = 'creative_canvas'
    primary_key = 'canvas_id'

    @classmethod
    def create_canvas(cls, user_id: int, program_id: int,
                      assets: Optional[str] = None) -> int:
        """Create creative canvas"""
        data = {
            'user_id': user_id,
            'program_id': program_id
        }

        if assets:
            data['assets'] = assets

        return cls.insert(data)

    @classmethod
    def update_canvas(cls, canvas_id: int, assets: str) -> int:
        """Update creative canvas"""
        return cls.update(canvas_id, {'assets': assets})

    @classmethod
    def get_user_canvases(cls, user_id: int) -> List[Dict[str, Any]]:
        """Get user's creative canvases"""
        query = """
                SELECT cc.*, p.program_name
                FROM creative_canvas cc
                         JOIN programs p ON cc.program_id = p.program_id
                WHERE cc.user_id = %s
                ORDER BY cc.updated_at DESC \
                """
        return db.execute_query(query, (user_id,))

    @classmethod
    def get_program_canvases(cls, program_id: int) -> List[Dict[str, Any]]:
        """Get all creative canvases for a program"""
        query = """
                SELECT cc.*, u.username as creator_name
                FROM creative_canvas cc
                         JOIN users u ON cc.user_id = u.user_id
                WHERE cc.program_id = %s
                ORDER BY cc.updated_at DESC \
                """
        return db.execute_query(query, (program_id,))


class Message(BaseModel):
    """Message model"""

    table_name = 'messages'
    primary_key = 'message_id'

    @classmethod
    def send_message(cls, sender_id: int, recipient_id: int, message_text: str) -> int:
        """Send message"""
        data = {
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'message_text': message_text
        }

        return cls.insert(data)

    @classmethod
    def mark_as_read(cls, message_id: int) -> int:
        """Mark message as read"""
        query = f"UPDATE {cls.table_name} SET read_at = NOW() WHERE message_id = %s"
        return db.execute_update(query, (message_id,))

    @classmethod
    def get_conversation(cls, user_id1: int, user_id2: int) -> List[Dict[str, Any]]:
        """Get conversation between two users"""
        query = """
                SELECT m.*,
                       u1.username as sender_name,
                       u2.username as recipient_name
                FROM messages m
                         JOIN users u1 ON m.sender_id = u1.user_id
                         JOIN users u2 ON m.recipient_id = u2.user_id
                WHERE (m.sender_id = %s AND m.recipient_id = %s)
                   OR (m.sender_id = %s AND m.recipient_id = %s)
                ORDER BY m.sent_at ASC \
                """
        return db.execute_query(query, (user_id1, user_id2, user_id2, user_id1))

    @classmethod
    def get_user_messages(cls, user_id: int, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get user's messages"""
        if unread_only:
            query = """
                    SELECT m.*, u.username as sender_name
                    FROM messages m
                             JOIN users u ON m.sender_id = u.user_id
                    WHERE m.recipient_id = %s \
                      AND m.read_at IS NULL
                    ORDER BY m.sent_at DESC \
                    """
        else:
            query = """
                    SELECT m.*, u.username as sender_name
                    FROM messages m
                             JOIN users u ON m.sender_id = u.user_id
                    WHERE m.recipient_id = %s
                    ORDER BY m.sent_at DESC \
                    """

        return db.execute_query(query, (user_id,))

    @classmethod
    def get_sent_messages(cls, user_id: int) -> List[Dict[str, Any]]:
        """Get messages sent by user"""
        query = """
                SELECT m.*, u.username as recipient_name
                FROM messages m
                         JOIN users u ON m.recipient_id = u.user_id
                WHERE m.sender_id = %s
                ORDER BY m.sent_at DESC \
                """
        return db.execute_query(query, (user_id,))


class Note(BaseModel):
    """Note model"""

    table_name = 'notes'
    primary_key = 'note_id'

    TARGET_SUBMISSION = 'submission'
    TARGET_CONTENT = 'content'
    TARGET_SIGHTING = 'sighting'

    @classmethod
    def create_note(cls, teacher_id: int, target_type: str,
                    target_id: int, note_text: str) -> int:
        """Create note"""
        data = {
            'teacher_id': teacher_id,
            'target_type': target_type,
            'target_id': target_id,
            'note_text': note_text
        }

        return cls.insert(data)

    @classmethod
    def get_target_notes(cls, target_type: str, target_id: int) -> List[Dict[str, Any]]:
        """Get all notes of the target"""
        query = """
                SELECT n.*, u.username as teacher_name
                FROM notes n
                         JOIN users u ON n.teacher_id = u.user_id
                WHERE n.target_type = %s \
                  AND n.target_id = %s
                ORDER BY n.created_at DESC \
                """
        return db.execute_query(query, (target_type, target_id))

    @classmethod
    def get_teacher_notes(cls, teacher_id: int) -> List[Dict[str, Any]]:
        """Get all notes of the teacher"""
        query = f"SELECT * FROM {cls.table_name} WHERE teacher_id = %s ORDER BY created_at DESC"
        return db.execute_query(query, (teacher_id,))
