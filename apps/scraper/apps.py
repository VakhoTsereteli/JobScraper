from django.apps import AppConfig
from .get_jobs import bog, jobs_ge


class ScraperConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scraper"
    
    def ready(self):
        pass
