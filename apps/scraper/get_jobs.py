import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse, parse_qs
from .models import Job



def bog():
    bog_jobs_url = "https://jsc-bank-of-georgia.hirehive.com"
    req = requests.get(f"{bog_jobs_url}/?q=web&CountryCode=&Category=ინფორმაციული+ტექნოლოგიები#jobs")

    soup = BS(req.text, "html.parser")
    jobs_list = soup.find("div", class_="hh-job-group")
    jobs = jobs_list.find_all("a")

    for job in jobs:
        job_id = job.get("href")[1:]

        if not Job.objects.filter(id=job_id).exists():
            job_detail_req = requests.get(f"{bog_jobs_url}/{job_id}")
            details = BS(job_detail_req.text, "html.parser")

            new_job = Job(
                id = job_id,
                title = details.find("h1", class_="hh-job-title").text.strip(),
                description = details.find("div", class_="hh-job-description").decode_contents(),
                company_name = "BOG",
                location = details.find("div", class_="hh-job-location").text.strip(),
                source_url = f"{bog_jobs_url}/{job_id}",
                source_website = "jsc-bank-of-georgia.hirehive.com"
            )
            new_job.save()
    print("BOG Jobs Scraped")
            
            
            
def jobs_ge():
    jobs_ge_url = "https://jobs.ge"
    req = requests.get(f"{jobs_ge_url}/?page=1&q=web&cid=6&lid=1")

    soup = BS(req.text, "html.parser")

    jobs_table = soup.find("table", id="job_list_table")
    jobs_tr = jobs_table.find_all("tr")

    for tr in jobs_tr:
        a_tags = tr.find_all("a")
        
        if len(a_tags) > 1:
            job_id = a_tags[0].get("href").replace("amp;","")[1:]
            
            if not Job.objects.filter(id=job_id).exists():
                job_details_req = requests.get(f"{jobs_ge_url}/{job_id}")
                details = BS(job_details_req.text, "html.parser")

                details_table = details.find("table", class_="dtable")
                details_tr = details_table.find_all("tr")

                if details_tr[3].find("a").text.strip() == "ინგლისურ ენაზე":
                    job_id = details_tr[3].find("a").get("href").replace("amp;","")[1:]
                    job_details_req = requests.get(f"{jobs_ge_url}/{job_id}")
                    details = BS(job_details_req.text, "html.parser")
                    details_table = details.find("table", class_="dtable")
                    details_tr = details_table.find_all("tr")

                if len(details_tr) > 0:
                    new_job = Job(
                        id=parse_qs(urlparse(f"{job_id}").query).get('id', [None])[0],
                        title = details_tr[0].find("b").text.strip(),
                        company_name = details_tr[1].find("b").text.strip(),
                        description = details_tr[3].decode_contents(),
                        location = "Tbilisi, Georgia",
                        source_url = f"{jobs_ge_url}/{job_id}",
                        source_website = "jobs.ge"
                    )
                    new_job.save()


    print("Jobs.ge Jobs Scraped")
