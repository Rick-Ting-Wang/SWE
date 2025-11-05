"""
Content-related models for content library and species sightings
"""
from typing import Optional, List, Dict, Any
from models import BaseModel


class ContentModel(BaseModel):
    """Content model for content library operations"""

    def upload_content(self, title: str, content_type: str, content_data: str,
                      created_by: int, org_id: Optional[int], is_public: bool) -> int:
        """Upload content to library"""
        return self._execute_insert(
            """INSERT INTO content_library (title, content_type, content_data,
                   created_by, org_id, is_public)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (title, content_type, content_data, created_by, org_id, is_public)
        )


class SightingModel(BaseModel):
    """Sighting model for species sighting operations"""

    def report_sighting(self, species_name: str, location: str, date_time: str,
                       description: str, photo_path: Optional[str], reported_by: int) -> int:
        """Report species sighting"""
        return self._execute_insert(
            """INSERT INTO species_sightings (species_name, location, date_time,
                   description, photo_path, reported_by)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (species_name, location, date_time, description, photo_path, reported_by)
        )


class AnalyticsModel(BaseModel):
    """Analytics model for business analytics operations"""

    def record_analytics(self, metric_type: str, metric_value: float,
                        metric_data: Optional[str] = None) -> int:
        """Record analytics data"""
        return self._execute_insert(
            """INSERT INTO business_analytics (metric_type, metric_value, metric_data)
               VALUES (%s, %s, %s)""",
            (metric_type, metric_value, metric_data)
        )


class CanvasModel(BaseModel):
    """Canvas model for creative canvas operations"""

    def save_canvas(self, user_id: int, program_id: int, assets: str) -> bool:
        """Save creative canvas"""
        try:
            self._execute_insert(
                """INSERT INTO creative_canvas (user_id, program_id, assets)
                   VALUES (%s, %s, %s) ON DUPLICATE KEY
                   UPDATE assets = %s, updated_at = NOW()""",
                (user_id, program_id, assets, assets)
            )
            return True
        except Exception:
            return False