from celery import shared_task
from .job_processor import JobProcessor

@shared_task
def get_jobs():
    JobProcessor.GetJobs.bog()
    JobProcessor.GetJobs.jobs_ge()
    
@shared_task
def send_emails():
    JobProcessor.Mail.send()