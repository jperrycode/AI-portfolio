
from django.db import models
from django.utils import timezone

class PersonalInformation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Education(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='educations')
    school_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.school_name} ({self.degree})"

class Project(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    technologies_used = models.CharField(max_length=255, blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

class Certification(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=50, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
