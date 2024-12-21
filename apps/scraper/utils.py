from .models import Job

def job_exists(job_id):
    return Job.objects.filter(id=job_id).exists()