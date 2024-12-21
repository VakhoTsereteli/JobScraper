import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse
from .models import Job



def bog():
    bog_jobs_url = "https://jsc-bank-of-georgia.hirehive.com"
    req = requests.get(f"{bog_jobs_url}/?q=web&CountryCode=&Category=ინფორმაციული+ტექნოლოგიები#jobs")

    soup = BS(req.text, "html.parser")
    jobs_list = soup.find("div", class_="hh-job-group")
    jobs = jobs_list.find_all("a")

    for job in jobs:
        job_id = job.get("href")[1:]

        if Job.objects.filter(id=job_id).exists() != True:
            job_detail_req = requests.get(f"{bog_jobs_url}/{job_id}")
            details = BS(job_detail_req.text, "html.parser")

            new_job = Job(
                id = job_id,
                title = details.find("h1", class_="hh-job-title").text.strip(),
                description = details.find("div", class_="hh-job-description").decode_contents(),
                company_name = "BOG",
                location = details.find("div", class_="hh-job-location").text.strip(),
                source_url = f"{bog_jobs_url}/{job_id}",
                source_website = urlparse(bog_jobs_url).netloc
            )
            new_job.save()

        




def jobs_ge():
    pass