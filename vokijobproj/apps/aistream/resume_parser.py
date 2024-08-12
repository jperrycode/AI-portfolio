from apps.aistream.models import PersonalInformation, Certification, Skill, Education, WorkExperience, ParsedResume

def parse_certifications(certifications_data, personal_info):
    certification_instances = []
    for cert_data in certifications_data:
        certification, created = Certification.objects.get_or_create(
            personal_info=personal_info,
            name=cert_data.get('name'),
            defaults={
                'issuing_organization': cert_data.get('issuing_organization'),
                'issue_date': cert_data.get('issue_date'),
                'expiration_date': cert_data.get('expiration_date'),
                'credential_id': cert_data.get('credential_id'),
                'credential_url': cert_data.get('credential_url'),
            }
        )
        certification_instances.append(certification)
    return certification_instances

def parse_skills(skills_data, personal_info):
    skill_instances = []
    for skill_data in skills_data:
        skill, created = Skill.objects.get_or_create(
            personal_info=personal_info,
            name=skill_data.get('name'),
            defaults={
                'proficiency': skill_data.get('proficiency'),
            }
        )
        skill_instances.append(skill)
    return skill_instances

def parse_education(education_data, personal_info):
    education_instances = []
    for edu_data in education_data:
        education, created = Education.objects.get_or_create(
            personal_info=personal_info,
            school_name=edu_data.get('school_name'),
            defaults={
                'degree': edu_data.get('degree'),
                'field_of_study': edu_data.get('field_of_study'),
                'start_date': edu_data.get('start_date'),
                'end_date': edu_data.get('end_date'),
                'grade': edu_data.get('grade'),
                'description': edu_data.get('description'),
            }
        )
        education_instances.append(education)
    return education_instances

def parse_work_experience(work_experience_data, personal_info):
    work_experience_instances = []
    for work_data in work_experience_data:
        work_experience, created = WorkExperience.objects.get_or_create(
            personal_info=personal_info,
            job_title=work_data.get('job_title'),
            company_name=work_data.get('company_name'),
            defaults={
                'location': work_data.get('location'),
                'start_date': work_data.get('start_date'),
                'end_date': work_data.get('end_date'),
                'description': work_data.get('description'),
            }
        )
        work_experience_instances.append(work_experience)
    return work_experience_instances

def parse_resume(resume_data):
    personal_info_data = resume_data.get('personal_info', {})
    first_name = personal_info_data.get('first_name')
    last_name = personal_info_data.get('last_name')
    email = personal_info_data.get('email')

    personal_info, created = PersonalInformation.objects.get_or_create(
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    certifications = parse_certifications(resume_data.get('certifications', []), personal_info)
    skills = parse_skills(resume_data.get('skills', []), personal_info)
    education = parse_education(resume_data.get('education', []), personal_info)
    work_experience = parse_work_experience(resume_data.get('work_experience', []), personal_info)

    parsed_resume, created = ParsedResume.objects.get_or_create(personal_info=personal_info)
    parsed_resume.certifications.set(certifications)
    parsed_resume.skills.set(skills)
    parsed_resume.education.set(education)
    parsed_resume.work_experience.set(work_experience)
    parsed_resume.save()

    return parsed_resume
