from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("job/<str:source_website>/<str:job_id>/", views.job_details, name="job_details")
]
