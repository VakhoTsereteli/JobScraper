from django.apps import AppConfig
import os

class ScraperConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scraper"
    
    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
        from .job_processor import JobProcessor
        JobProcessor.GetJobs.bog()
        JobProcessor.GetJobs.jobs_ge()
        JobProcessor.Mail.send()