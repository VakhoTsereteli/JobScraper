# Generated by Django 5.1.4 on 2024-12-23 02:49

import apps.scraper.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0012_alter_job_scraped_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='scraped_date',
            field=models.CharField(default=apps.scraper.models.get_current_date, max_length=255),
        ),
    ]
