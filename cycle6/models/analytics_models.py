"""
Komodo Hub - Analytics and Log Models
Analytics and Access Log models
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from database import BaseModel, db
import json


class AccessLog(BaseModel):
    """Access log model"""

    table_name = 'access_logs'
    primary_key = 'log_id'

    @classmethod
    def log_action(cls, user_id: Optional[int], action: str,
                   target_type: Optional[str] = None,
                   target_id: Optional[int] = None,
                   ip_address: Optional[str] = None) -> int:
        """Record user action"""
        data = {
            'action': action
        }

        if user_id:
            data['user_id'] = user_id
        if target_type:
            data['target_type'] = target_type
        if target_id:
            data['target_id'] = target_id
        if ip_address:
            data['ip_address'] = ip_address

        return cls.insert(data)

    @classmethod
    def get_user_logs(cls, user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user's operation logs"""
        query = f"SELECT * FROM {cls.table_name} WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s"
        return db.execute_query(query, (user_id, limit))

    @classmethod
    def get_logs_by_action(cls, action: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get logs by action type"""
        query = f"SELECT * FROM {cls.table_name} WHERE action = %s ORDER BY timestamp DESC LIMIT %s"
        return db.execute_query(query, (action, limit))

    @classmethod
    def get_logs_by_date_range(cls, start_date: datetime, end_date: datetime,
                               user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get logs by date range"""
        if user_id:
            query = f"""
                SELECT * FROM {cls.table_name} 
                WHERE timestamp BETWEEN %s AND %s AND user_id = %s
                ORDER BY timestamp DESC
            """
            return db.execute_query(query, (start_date, end_date, user_id))
        else:
            query = f"""
                SELECT * FROM {cls.table_name} 
                WHERE timestamp BETWEEN %s AND %s
                ORDER BY timestamp DESC
            """
            return db.execute_query(query, (start_date, end_date))

    @classmethod
    def get_activity_summary(cls, days: int = 7) -> Dict[str, Any]:
        """Get summary of activities in the past N days"""
        start_date = datetime.now() - timedelta(days=days)

        query = """
                SELECT
                    action, COUNT (*) as count, COUNT (DISTINCT user_id) as unique_users
                FROM access_logs
                WHERE timestamp >= %s
                GROUP BY action
                ORDER BY count DESC \
                """

        results = db.execute_query(query, (start_date,))

        return {
            'period_days': days,
            'start_date': start_date.isoformat(),
            'activities': results
        }

    @classmethod
    def get_student_data_access_audit(cls, student_id: int) -> List[Dict[str, Any]]:
        """Audit student data access (security compliance)"""
        query = """
                SELECT al.*, u.username as accessor_name, u.user_type
                FROM access_logs al
                         LEFT JOIN users u ON al.user_id = u.user_id
                WHERE al.target_type IN ('submission', 'assessment', 'student_profile')
                  AND al.target_id = %s
                ORDER BY al.timestamp DESC \
                """
        return db.execute_query(query, (student_id,))


class BusinessAnalytics(BaseModel):
    """Business analytics model"""

    table_name = 'business_analytics'
    primary_key = 'analytics_id'

    # Metric type constants
    DAILY_ACTIVE_USERS = 'daily_active_users'
    MONTHLY_ACTIVE_USERS = 'monthly_active_users'
    NEW_REGISTRATIONS = 'new_registrations'
    SUBSCRIPTION_REVENUE = 'subscription_revenue'
    PROGRAM_ENROLLMENTS = 'program_enrollments'
    CONTENT_UPLOADS = 'content_uploads'
    SPECIES_SIGHTINGS = 'species_sightings'
    SUBMISSION_RATE = 'submission_rate'
    ASSESSMENT_COMPLETION_RATE = 'assessment_completion_rate'

    @classmethod
    def record_metric(cls, metric_type: str, metric_value: float,
                      metric_data: Optional[Dict] = None) -> int:
        """Record business metric"""
        data = {
            'metric_type': metric_type,
            'metric_value': metric_value
        }

        if metric_data:
            data['metric_data'] = json.dumps(metric_data)

        return cls.insert(data)

    @classmethod
    def get_metric_history(cls, metric_type: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get historical data for a metric"""
        start_date = datetime.now() - timedelta(days=days)

        query = f"""
            SELECT * FROM {cls.table_name}
            WHERE metric_type = %s AND recorded_at >= %s
            ORDER BY recorded_at DESC
        """
        return db.execute_query(query, (metric_type, start_date))

    @classmethod
    def get_latest_metrics(cls) -> Dict[str, Any]:
        """Get the latest values of all metrics"""
        query = """
                SELECT ba1.*
                FROM business_analytics ba1
                         INNER JOIN (SELECT metric_type, MAX(recorded_at) as max_date \
                                     FROM business_analytics \
                                     GROUP BY metric_type) ba2 ON ba1.metric_type = ba2.metric_type
                    AND ba1.recorded_at = ba2.max_date \
                """

        results = db.execute_query(query)

        # Format as dict
        metrics = {}
        for row in results:
            metric_type = row['metric_type']
            metrics[metric_type] = {
                'value': float(row['metric_value']),
                'data': json.loads(row['metric_data']) if row.get('metric_data') else None,
                'recorded_at': row['recorded_at'].isoformat() if row.get('recorded_at') else None
            }

        return metrics

    @classmethod
    def calculate_daily_active_users(cls) -> int:
        """Calculate number of daily active users"""
        today = date.today()
        query = """
                SELECT COUNT(DISTINCT user_id) as count
                FROM access_logs
                WHERE DATE (timestamp) = %s \
                """
        result = db.execute_query(query, (today,))
        count = result[0]['count'] if result else 0

        # Record metric
        cls.record_metric(cls.DAILY_ACTIVE_USERS, count)

        return count

    @classmethod
    def calculate_user_demographics(cls) -> Dict[str, int]:
        """Calculate user demographics"""
        query = """
                SELECT user_type, COUNT(*) as count
                FROM users
                GROUP BY user_type \
                """

        results = db.execute_query(query)
        demographics = {row['user_type']: row['count'] for row in results}

        # Record metric
        total_users = sum(demographics.values())
        cls.record_metric('total_users', total_users, demographics)

        return demographics

    @classmethod
    def calculate_program_popularity(cls) -> List[Dict[str, Any]]:
        """Calculate program popularity"""
        query = """
                SELECT p.program_id, \
                       p.program_name, \
                       p.program_type, \
                       COUNT(pe.enrollment_id) as enrollment_count
                FROM programs p
                         LEFT JOIN program_enrollments pe ON p.program_id = pe.program_id
                WHERE pe.status = 'active'
                GROUP BY p.program_id, p.program_name, p.program_type
                ORDER BY enrollment_count DESC \
                """

        results = db.execute_query(query)

        # Record metric
        if results:
            top_program = results[0]
            cls.record_metric(
                'most_popular_program',
                top_program['enrollment_count'],
                {
                    'program_id': top_program['program_id'],
                    'program_name': top_program['program_name'],
                    'program_type': top_program['program_type']
                }
            )

        return results

    @classmethod
    def calculate_subscription_statistics(cls) -> Dict[str, Any]:
        """Calculate subscription statistics"""
        query = """
                SELECT org_type, \
                       subscription_status, \
                       COUNT(*) as count
                FROM organizations
                GROUP BY org_type, subscription_status \
                """

        results = db.execute_query(query)

        stats = {}
        total_active = 0

        for row in results:
            org_type = row['org_type']
            status = row['subscription_status']
            count = row['count']

            if org_type not in stats:
                stats[org_type] = {}
            stats[org_type][status] = count

            if status == 'active':
                total_active += count

        # Record metric
        cls.record_metric('active_subscriptions', total_active, stats)

        return stats

    @classmethod
    def calculate_content_statistics(cls) -> Dict[str, Any]:
        """Calculate content statistics"""
        query = """
                SELECT content_type, \
                       is_public, \
                       COUNT(*) as count
                FROM content_library
                GROUP BY content_type, is_public \
                """

        results = db.execute_query(query)

        stats = {
            'by_type': {},
            'public_count': 0,
            'private_count': 0,
            'total_count': 0
        }

        for row in results:
            content_type = row['content_type']
            is_public = row['is_public']
            count = row['count']

            if content_type not in stats['by_type']:
                stats['by_type'][content_type] = {'public': 0, 'private': 0}

            if is_public:
                stats['by_type'][content_type]['public'] = count
                stats['public_count'] += count
            else:
                stats['by_type'][content_type]['private'] = count
                stats['private_count'] += count

            stats['total_count'] += count

        # Record metric
        cls.record_metric('total_content_items', stats['total_count'], stats)

        return stats

    @classmethod
    def generate_dashboard_data(cls) -> Dict[str, Any]:
        """Generate dashboard data (admin view)"""
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'user_demographics': cls.calculate_user_demographics(),
            'subscription_stats': cls.calculate_subscription_statistics(),
            'program_popularity': cls.calculate_program_popularity()[:10],  # Top 10
            'content_stats': cls.calculate_content_statistics(),
            'daily_active_users': cls.calculate_daily_active_users(),
            'latest_metrics': cls.get_latest_metrics()
        }

        return dashboard
