import requests
from bs4 import BeautifulSoup as BS
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from dotenv import load_dotenv
import os
import re
from .models import Job

load_dotenv()

class JobProcessor:
    
    class GetJobs:
        @staticmethod
        def bog():
            try:
                bog_jobs_url = "https://jsc-bank-of-georgia.hirehive.com"
                req = requests.get(f"{bog_jobs_url}/?q=web&CountryCode=&Category=ინფორმაციული+ტექნოლოგიები#jobs")
                req.raise_for_status()

                soup = BS(req.text, "html.parser")
                jobs_list = soup.find("div", class_="hh-job-group")
                jobs = jobs_list.find_all("a")

                if jobs:
                    for job in jobs:
                        try:
                            job_id = job.get("href")[1:]

                            if not Job.objects.filter(id=job_id).exists():
                                job_detail_req = requests.get(f"{bog_jobs_url}/{job_id}")
                                job_detail_req.raise_for_status()
                                details = BS(job_detail_req.text, "html.parser")

                                new_job = Job(
                                    id=job_id,
                                    title=details.find("h1", class_="hh-job-title").text.strip(),
                                    description=details.find("div", class_="hh-job-description").decode_contents(),
                                    company_name="BOG",
                                    location=details.find("div", class_="hh-job-location").text.strip(),
                                    source_url=f"{bog_jobs_url}/{job_id}",
                                    source_website="jsc-bank-of-georgia.hirehive.com"
                                )
                                new_job.save()
                        except Exception as e:
                            print(f"Error processing job {job_id}: {e}")

                print("BOG Jobs Scraped")
            except Exception as e:
                print(f"Error scraping BOG jobs: {e}")


        @staticmethod
        def jobs_ge():
            try:
                jobs_ge_url = "https://jobs.ge"
                req = requests.get(f"{jobs_ge_url}/?page=1&q=web&cid=6&lid=1")
                

                soup = BS(req.text, "html.parser")

                jobs_table = soup.find("table", id="job_list_table")
                jobs_tr = jobs_table.find_all("tr")
                
                if jobs_tr:
                    for tr in jobs_tr[1:]:
                        id = re.search(r"\d+", tr.find("a").get("href")).group()
                        
                        if not Job.objects.filter(id=id).exists():
                            try:
                                req = requests.get(f"{jobs_ge_url}/{tr.find('a').get('href')}")
                                req.raise_for_status()
                                job_soup = BS(req.text, "html.parser")
                                details = job_soup.find("table", class_="dtable")
                                details_tr = details.find_all("tr")
                                
                                if len(details_tr)>0 and details_tr[3].find("a").text.strip()=="ინგლისურ ენაზე":
                                    req = requests.get(f"{jobs_ge_url}/{details_tr[3].find('a').get('href')}")
                                    req.raise_for_status()
                                    job_soup = BS(req.text, "html.parser")
                                    details = job_soup.find("table", class_="dtable")
                                    details_tr = details.find_all("tr")
                                    
                                    if len(details_tr)>0:
                                        new_job = Job(
                                            id=id,
                                            title=details_tr[0].find("b").text.strip(),
                                            company_name=details_tr[1].find("b").text.strip(),
                                            description=details_tr[3].decode_contents(),
                                            location = "Tbilisi, Georgia",
                                            source_url=f"{jobs_ge_url}/en/?view=jobs&id={id}",
                                            source_website="jobs.ge"
                                        )
                                        new_job.save()
                                new_job = Job(
                                            id=id,
                                            title=details_tr[0].find("b").text.strip(),
                                            company_name=details_tr[1].find("b").text.strip(),
                                            description=details_tr[3].decode_contents(),
                                            location = "Tbilisi, Georgia",
                                            source_url=f"{jobs_ge_url}/{tr.find('a').get('href')[1:]}",
                                            source_website="jobs.ge"
                                        )
                                new_job.save()   
                                print("Jobs.ge Jobs Scraped")  
                            except Exception as e:
                                print(f"Error processing job {id}: {e}") 
                        else:
                            print("Job already exists")                      
            except Exception as e:
                print(f"Error scraping jobs.ge jobs: {e}")
    
    
    class Mail:
        @staticmethod
        def send():
            unsent_jobs = Job.objects.filter(sent=False)
            if len(unsent_jobs) > 0:
                for job in unsent_jobs:
                    JobProcessor.Mail.send_email(job)
            else:
                print("No new jobs to send")
            
        @staticmethod    
        def send_email(job: Job):
            html_body = render_to_string("emails/job_alert.html", {"job": job})
            email = EmailMessage(
                subject="NEW JOB ALERT",
                body=html_body,
                from_email=os.getenv("EMAIL_HOST_USER"),
                to=[os.getenv("EMAIL_HOST_USER")]
            )
            email.content_subtype = "html"
            try:
                email.send()
                job.sent = True
                job.save()
                print("Email sent")
            except Exception as e:
                print(f"Error sending email: {e}")