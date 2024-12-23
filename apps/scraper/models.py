from django.db import models
from django.utils import timezone
import pytz

def get_current_date():
    local_tz = pytz.timezone('Asia/Tbilisi')
    return timezone.now().astimezone(local_tz).strftime("%d-%m-%Y")

class Job(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, null=False)
    source_url = models.URLField()
    source_website = models.CharField(max_length=255, null=False)
    scraped_date = models.CharField(max_length=255, null=False, default=get_current_date)
    sent = models.BooleanField(default=False)    