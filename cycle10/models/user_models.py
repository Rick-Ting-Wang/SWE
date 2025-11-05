"""
User-related models and operations
"""
from typing import Optional, List, Dict, Any
from models import BaseModel, DatabaseManager


class UserModel(BaseModel):
    """User model for user-related operations"""

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        result = self._execute_query(
            "SELECT * FROM users WHERE user_id = %s", (user_id,)
        )
        return result[0] if result else None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        result = self._execute_query(
            "SELECT * FROM users WHERE email = %s", (email,)
        )
        return result[0] if result else None

    def create_user(self, username: str, email: str, password_hash: str,
                   user_type: str, user_image: str = '1') -> int:
        """Create a new user"""
        user_id = self._execute_insert(
            """INSERT INTO users (user_image, username, email, password, user_type)
               VALUES (%s, %s, %s, %s, %s)""",
            (user_image, username, email, password_hash, user_type)
        )

        # Create user profile
        self._execute_insert(
            "INSERT INTO user_profiles (user_id) VALUES (%s)", (user_id,)
        )

        return user_id

    def update_last_login(self, user_id: int):
        """Update user's last login time"""
        self._execute_update(
            "UPDATE users SET last_login = NOW() WHERE user_id = %s", (user_id,)
        )

    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get user profile with combined user and profile data"""
        result = self._execute_query(
            """SELECT u.user_id, u.username, u.email, u.user_type, u.user_image,
                      u.created_at, u.last_login, p.avatar_path, p.color_scheme,
                      p.bio, p.is_public
               FROM users u
               LEFT JOIN user_profiles p ON u.user_id = p.user_id
               WHERE u.user_id = %s""",
            (user_id,)
        )
        return result[0] if result else {}


class OrganizationModel(BaseModel):
    """Organization model for organization-related operations"""

    def create_organization(self, org_type: str, org_name: str,
                          org_profile: Optional[str], is_public: bool) -> int:
        """Create a new organization"""
        return self._execute_insert(
            """INSERT INTO organizations (org_type, org_name, org_profile, is_public)
               VALUES (%s, %s, %s, %s)""",
            (org_type, org_name, org_profile, is_public)
        )

    def add_organization_member(self, org_id: int, user_id: int, role: str,
                               access_code: Optional[str] = None) -> bool:
        """Add user to organization"""
        try:
            self._execute_insert(
                """INSERT INTO organization_members (org_id, user_id, role, access_code, joined_date)
                   VALUES (%s, %s, %s, %s, CURDATE())""",
                (org_id, user_id, role, access_code)
            )
            return True
        except Exception:
            return False

    def get_user_organizations(self, user_id: int) -> List[Dict[str, Any]]:
        """Get organizations user belongs to"""
        return self._execute_query(
            """SELECT o.org_id, o.org_name, o.org_type, om.role
               FROM organization_members om
               JOIN organizations o ON om.org_id = o.org_id
               WHERE om.user_id = %s""",
            (user_id,)
        )


class MessageModel(BaseModel):
    """Message model for message-related operations"""

    def send_message(self, sender_id: int, recipient_id: int, message_text: str) -> int:
        """Send a message"""
        return self._execute_insert(
            """INSERT INTO messages (sender_id, recipient_id, message_text)
               VALUES (%s, %s, %s)""",
            (sender_id, recipient_id, message_text)
        )

    def get_received_messages(self, user_id: int) -> List[Dict[str, Any]]:
        """Get messages received by user"""
        return self._execute_query(
            """SELECT m.message_id, m.message_text, m.sent_at,
                      u.username AS sender_name, u.user_id AS sender_id
               FROM messages m
               LEFT JOIN users u ON m.sender_id = u.user_id
               WHERE m.recipient_id = %s
               ORDER BY m.sent_at DESC""",
            (user_id,)
        )