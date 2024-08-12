from django.db import models
from django.utils import timezone

class PersonalInformation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name_plural = "Personal Information"
        verbose_name = ("Personal Information")

class Education(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='education')
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.school_name}"

class WorkExperience(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='work_experience')
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Skill(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.proficiency})"

class Project(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    technologies_used = models.CharField(max_length=255)
    project_url = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class Certification(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

class Language(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.proficiency})"

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

class Award(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='awards')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_awarded = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Award"
        verbose_name_plural = "Awards"

class Publication(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=255)
    publication_name = models.CharField(max_length=255)
    publication_date = models.DateField()
    description = models.TextField()
    publication_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

class VolunteerExperience(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='volunteer_experience')
    role = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.role} at {self.organization_name}"
    class Meta:
        verbose_name = "Volunteer Experience"
        verbose_name_plural = "Volunteer Experiences"


class ClaudeResponse(models.Model):
    response_id = models.CharField(max_length=100, null=False, blank=False)
    response_type = models.CharField(max_length=20, null=False, blank=False)
    response_date = models.DateTimeField(auto_now_add=True)
    response_content_type = models.CharField(max_length=20, null=False, blank=False)
    response_content_text = models.TextField(null=False, blank=False)
    response_model = models.CharField(max_length=100, null=False, blank=False)
    response_stop_reason = models.CharField(max_length=30, null=False, blank=False)
    response_stop_sequence = models.CharField(max_length=100, null=False, blank=False)
    response_usage_input_tokens = models.IntegerField(default=0)
    response_usage_output_tokens = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.response_id} - {self.response_type}"

    class Meta:
        verbose_name = "Claude Response"
        verbose_name_plural = "Claude Responses"

class ParsedResume(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='parsed_resumes')
    certifications = models.ManyToManyField(Certification, related_name='parsed_resumes')
    skills = models.ManyToManyField(Skill, related_name='parsed_resumes')
    education = models.ManyToManyField(Education, related_name='parsed_resumes')
    work_experience = models.ManyToManyField(WorkExperience, related_name='parsed_resumes')

    def __str__(self):
        return f"Parsed Resume for {self.personal_info.first_name} {self.personal_info.last_name}"