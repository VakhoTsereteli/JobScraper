# views.py
from django.shortcuts import render, get_object_or_404
from ..scraper.models import Job
from itertools import groupby



def home(request):
    jobs = Job.objects.order_by('source_website')
    grouped_jobs = {}
    for key, group in groupby(jobs, lambda x: x.source_website):
        grouped_jobs[key] = list(group)

    return render(request, 'pages/index.html', {'grouped_jobs': grouped_jobs})

def job_details(request,source_website, job_id):

    job = get_object_or_404(Job,source_website=source_website, id=job_id)

    return render(request, "pages/job_details.html", {"job": job})