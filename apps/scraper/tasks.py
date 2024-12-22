from celery import shared_task
from .get_jobs import bog, jobs_ge

@shared_task
def get_jobs():
    bog()   
    jobs_ge()