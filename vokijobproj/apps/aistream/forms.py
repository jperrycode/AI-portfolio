from django import forms
from .models import PersonalInformation, Education, Project, Certification

class ResumeUploadForm(forms.ModelForm):
    resume = forms.FileField(required=False)
    projects = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    schools = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    certifications = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = PersonalInformation
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'linkedin_profile', 'github_profile',
                  'personal_website', 'resume']

    def save(self, commit=True):
        instance = super().save(commit=False)
        resume_file = self.cleaned_data.get('resume')

        if resume_file:
            # Process the resume file
            resume_text = resume_file.read().decode('utf-8')
            extracted_data = extract_resume_data(resume_text)

            # Update personal information fields
            instance.first_name = extracted_data['personal_information'].get('first_name', instance.first_name)
            instance.last_name = extracted_data['personal_information'].get('last_name', instance.last_name)
            instance.email = extracted_data['personal_information'].get('email', instance.email)
            instance.phone_number = extracted_data['personal_information'].get('phone_number', instance.phone_number)
            instance.address = extracted_data['personal_information'].get('address', instance.address)
            instance.linkedin_profile = extracted_data['personal_information'].get('linkedin_profile',
                                                                                   instance.linkedin_profile)
            instance.github_profile = extracted_data['personal_information'].get('github_profile',
                                                                                 instance.github_profile)
            instance.personal_website = extracted_data['personal_information'].get('personal_website',
                                                                                   instance.personal_website)
            instance.save()

            # Update related entries
            self.update_related_entries(instance, extracted_data)

        if commit:
            instance.save()
        return instance

    def update_related_entries(self, instance, extracted_data):
        # Update projects
        projects_data = extracted_data.get('projects', [])
        for project_data in projects_data:
            Project.objects.create(
                personal_info=instance,
                title=project_data['title'],
                description=project_data['description'],
                technologies_used=project_data.get('technologies_used', ''),
                project_url=project_data.get('project_url', ''),
                start_date=project_data['start_date'],
                end_date=project_data.get('end_date', None)
            )

        # Update schools
        schools_data = extracted_data.get('education', [])
        for school_data in schools_data:
            Education.objects.create(
                personal_info=instance,
                school_name=school_data['school_name'],
                degree=school_data['degree'],
                field_of_study=school_data['field_of_study'],
                start_date=school_data['start_date'],
                end_date=school_data['end_date']
            )

        # Update certifications
        certs_data = extracted_data.get('certifications', [])
        for cert_data in certs_data:
            Certification.objects.create(
                personal_info=instance,
                name=cert_data['name'],
                issuing_organization=cert_data['issuing_organization'],
                issue_date=cert_data['issue_date'],
                expiration_date=cert_data.get('expiration_date', None),
                credential_id=cert_data.get('credential_id', ''),
                credential_url=cert_data.get('credential_url', '')
            )
