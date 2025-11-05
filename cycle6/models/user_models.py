"""
Komodo Hub - User and Organization Models
User and Organization models
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from database import BaseModel, db
import hashlib


class User(BaseModel):
    """User model"""

    table_name = 'users'
    primary_key = 'user_id'

    # User type constants
    ADMIN = 'admin'
    PRINCIPAL = 'principal'
    SCHOOL_ADMIN = 'school_admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    COMMUNITY_CHAIR = 'community_chair'
    COMMUNITY_MEMBER = 'community_member'
    PUBLIC = 'public'

    @classmethod
    def create_user(cls, username: str, email: str, password: str,
                    user_type: str, user_image: Optional[str] = None) -> int:
        """Create a new user"""
        # Password hash (should use bcrypt or similar in production)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        data = {
            'username': username,
            'email': email,
            'password': password_hash,
            'user_type': user_type
        }

        if user_image:
            data['user_image'] = user_image

        return cls.insert(data)

    @classmethod
    def find_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        query = f"SELECT * FROM {cls.table_name} WHERE email = %s"
        results = db.execute_query(query, (email,))
        return results[0] if results else None

    @classmethod
    def find_by_username(cls, username: str) -> Optional[Dict[str, Any]]:
        """Find user by username"""
        query = f"SELECT * FROM {cls.table_name} WHERE username = %s"
        results = db.execute_query(query, (username,))
        return results[0] if results else None

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional[Dict[str, Any]]:
        """User authentication"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = f"SELECT * FROM {cls.table_name} WHERE email = %s AND password = %s"
        results = db.execute_query(query, (email, password_hash))

        if results:
            # Update last login time
            user = results[0]
            cls.update_last_login(user['user_id'])
            return user
        return None

    @classmethod
    def update_last_login(cls, user_id: int):
        """Update last login time"""
        query = f"UPDATE {cls.table_name} SET last_login = NOW() WHERE user_id = %s"
        db.execute_update(query, (user_id,))

    @classmethod
    def get_users_by_type(cls, user_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user list by type"""
        return cls.find_by_condition({'user_type': user_type}, limit)

    @classmethod
    def get_user_organizations(cls, user_id: int) -> List[Dict[str, Any]]:
        """Get all organizations a user belongs to"""
        query = """
                SELECT o.*, om.role, om.joined_date
                FROM organizations o
                         JOIN organization_members om ON o.org_id = om.org_id
                WHERE om.user_id = %s \
                """
        return db.execute_query(query, (user_id,))


class Organization(BaseModel):
    """Organization model"""

    table_name = 'organizations'
    primary_key = 'org_id'

    # Organization type constants
    SCHOOL = 'school'
    COMMUNITY = 'community'

    # Subscription status constants
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'

    @classmethod
    def create_organization(cls, org_type: str, org_name: str,
                            org_profile: Optional[str] = None,
                            is_public: bool = True,
                            subscription_status: str = PENDING) -> int:
        """Create a new organization"""
        data = {
            'org_type': org_type,
            'org_name': org_name,
            'is_public': is_public,
            'subscription_status': subscription_status
        }

        if org_profile:
            data['org_profile'] = org_profile

        return cls.insert(data)

    @classmethod
    def update_subscription(cls, org_id: int, status: str,
                            subscription_date: Optional[date] = None):
        """Update subscription status"""
        data = {'subscription_status': status}
        if subscription_date:
            data['subscription_date'] = subscription_date
        elif status == cls.ACTIVE:
            data['subscription_date'] = date.today()

        return cls.update(org_id, data)

    @classmethod
    def get_by_type(cls, org_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get organization list by type"""
        return cls.find_by_condition({'org_type': org_type}, limit)

    @classmethod
    def get_active_subscriptions(cls, org_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get organizations with active subscription"""
        if org_type:
            query = f"SELECT * FROM {cls.table_name} WHERE subscription_status = 'active' AND org_type = %s"
            return db.execute_query(query, (org_type,))
        else:
            query = f"SELECT * FROM {cls.table_name} WHERE subscription_status = 'active'"
            return db.execute_query(query)

    @classmethod
    def get_public_organizations(cls) -> List[Dict[str, Any]]:
        """Get public organizations"""
        return cls.find_by_condition({'is_public': True}, limit=1000)

    @classmethod
    def get_organization_members(cls, org_id: int, role: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get organization members"""
        if role:
            query = """
                    SELECT u.*, om.role, om.joined_date, om.access_code
                    FROM users u
                             JOIN organization_members om ON u.user_id = om.user_id
                    WHERE om.org_id = %s \
                      AND om.role = %s \
                    """
            return db.execute_query(query, (org_id, role))
        else:
            query = """
                    SELECT u.*, om.role, om.joined_date, om.access_code
                    FROM users u
                             JOIN organization_members om ON u.user_id = om.user_id
                    WHERE om.org_id = %s \
                    """
            return db.execute_query(query, (org_id,))

    @classmethod
    def get_subscription_statistics(cls) -> Dict[str, Any]:
        """Get subscription statistics"""
        query = """
                SELECT org_type, \
                       subscription_status, \
                       COUNT(*) as count
                FROM organizations
                GROUP BY org_type, subscription_status \
                """
        results = db.execute_query(query)

        # Format results
        stats = {}
        for row in results:
            org_type = row['org_type']
            status = row['subscription_status']
            count = row['count']

            if org_type not in stats:
                stats[org_type] = {}
            stats[org_type][status] = count

        return stats


class OrganizationMember(BaseModel):
    """Organization member model"""

    table_name = 'organization_members'
    primary_key = 'membership_id'

    # Role constants
    PRINCIPAL = 'principal'
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    CHAIRMAN = 'chairman'
    MEMBER = 'member'

    @classmethod
    def add_member(cls, org_id: int, user_id: int, role: str,
                   access_code: Optional[str] = None,
                   joined_date: Optional[date] = None) -> int:
        """Add organization member"""
        data = {
            'org_id': org_id,
            'user_id': user_id,
            'role': role,
            'joined_date': joined_date or date.today()
        }

        if access_code:
            data['access_code'] = access_code

        return cls.insert(data)

    @classmethod
    def generate_access_code(cls, org_id: int, user_id: int) -> str:
        """Generate access code for student"""
        import uuid
        access_code = str(uuid.uuid4())[:8].upper()

        query = """
                UPDATE organization_members
                SET access_code = %s
                WHERE org_id = %s \
                  AND user_id = %s \
                """
        db.execute_update(query, (access_code, org_id, user_id))

        return access_code

    @classmethod
    def verify_access_code(cls, access_code: str) -> Optional[Dict[str, Any]]:
        """Verify access code"""
        query = f"SELECT * FROM {cls.table_name} WHERE access_code = %s"
        results = db.execute_query(query, (access_code,))
        return results[0] if results else None

    @classmethod
    def get_member_role(cls, org_id: int, user_id: int) -> Optional[str]:
        """Get user's role in the organization"""
        query = f"SELECT role FROM {cls.table_name} WHERE org_id = %s AND user_id = %s"
        results = db.execute_query(query, (org_id, user_id))
        return results[0]['role'] if results else None

    @classmethod
    def remove_member(cls, org_id: int, user_id: int) -> int:
        """Remove organization member"""
        query = f"DELETE FROM {cls.table_name} WHERE org_id = %s AND user_id = %s"
        return db.execute_update(query, (org_id, user_id))


class UserProfile(BaseModel):
    """User profile model"""

    table_name = 'user_profiles'
    primary_key = 'profile_id'

    @classmethod
    def create_profile(cls, user_id: int, avatar_path: Optional[str] = None,
                       color_scheme: Optional[str] = None,
                       bio: Optional[str] = None,
                       is_public: bool = True) -> int:
        """Create user profile"""
        data = {
            'user_id': user_id,
            'is_public': is_public
        }

        if avatar_path:
            data['avatar_path'] = avatar_path
        if color_scheme:
            data['color_scheme'] = color_scheme
        if bio:
            data['bio'] = bio

        return cls.insert(data)

    @classmethod
    def get_by_user_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """Get profile by user ID"""
        query = f"SELECT * FROM {cls.table_name} WHERE user_id = %s"
        results = db.execute_query(query, (user_id,))
        return results[0] if results else None

    @classmethod
    def update_profile(cls, user_id: int, data: Dict[str, Any]) -> int:
        """Update user profile"""
        query_parts = [f"{key} = %s" for key in data.keys()]
        query = f"UPDATE {cls.table_name} SET {', '.join(query_parts)} WHERE user_id = %s"
        params = tuple(data.values()) + (user_id,)
        return db.execute_update(query, params)

    @classmethod
    def get_public_profiles(cls, limit: int = 100) -> List[Dict[str, Any]]:
        """Get public user profiles"""
        query = """
                SELECT up.*, u.username, u.user_type
                FROM user_profiles up
                         JOIN users u ON up.user_id = u.user_id
                WHERE up.is_public = TRUE
                    LIMIT %s \
                """
        return db.execute_query(query, (limit,))
