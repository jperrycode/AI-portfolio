from django.core.management.base import BaseCommand
from myapp.models import PersonalInformation, ParsedResume

class Command(BaseCommand):
    help = 'Create ParsedResume instances from existing data'

    def handle(self, *args, **kwargs):
        personal_infos = PersonalInformation.objects.all()

        for info in personal_infos:
            parsed_resume, created = ParsedResume.objects.get_or_create(personal_info=info)

            parsed_resume.certifications.clear()
            parsed_resume.skills.clear()
            parsed_resume.education.clear()
            parsed_resume.work_experience.clear()

            certifications = info.certifications.all()
            skills = info.skills.all()
            education = info.education.all()
            work_experience = info.work_experience.all()

            parsed_resume.certifications.set(certifications)
            parsed_resume.skills.set(skills)
            parsed_resume.education.set(education)
            parsed_resume.work_experience.set(work_experience)
            parsed_resume.save()

        self.stdout.write(self.style.SUCCESS('Successfully created or updated parsed resume instances'))
