from django.db import models

class Job(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=False)
    source_url = models.URLField()
    source_website = models.CharField(max_length=255, null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
