"""
Utility functions for the application
"""
from typing import Optional, List
from flask import request
from models import DatabaseManager
from models.user_models import UserModel


def log_access(db_manager: DatabaseManager, user_id: Optional[int],
              action: str, target_type: Optional[str] = None,
              target_id: Optional[int] = None):
    """Log user access to database"""
    try:
        ip = request.remote_addr
        user_model = UserModel(db_manager)
        user_model._execute_insert(
            """INSERT INTO access_logs (user_id, action, target_type, target_id, ip_address)
               VALUES (%s, %s, %s, %s, %s)""",
            (user_id, action, target_type, target_id, ip)
        )
    except Exception as e:
        print(f"Failed to log access: {e}")


def require_role(db_manager: DatabaseManager, user_id: int, allowed_roles: List[str]) -> bool:
    """Check if user has required role"""
    try:
        user_model = UserModel(db_manager)
        user = user_model.get_user_by_id(user_id)
        return user and user['user_type'] in allowed_roles
    except Exception:
        return False


def get_user_types() -> List[str]:
    """Get available user types"""
    return [
        'admin', 'principal', 'school_admin',
        'teacher', 'student', 'community_chair',
        'community_member', 'public'
    ]


def get_program_types() -> List[str]:
    """Get available program types"""
    return ['internal', 'local', 'regional', 'national']


def get_activity_types() -> List[str]:
    """Get available activity types"""
    return ['in-class', 'outdoor', 'challenge', 'game', 'assessment']


def get_content_types() -> List[str]:
    """Get available content types"""
    return [
        'article', 'essay', 'report', 'sighting',
        'photo', 'video', 'educational_material'
    ]


def format_datetime(dt) -> str:
    """Format datetime for display"""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M')
    return 'Unknown'