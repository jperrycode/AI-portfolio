from celery import shared_task
import anthropic
from django.apps import apps
from .models import PersonalInformation, Education, WorkExperience, Skill, Project, Certification, ClaudeResponse

@shared_task
def parse_resume_task(document_id):
    Document = apps.get_model('fileintake', 'Document')

    try:
        document = Document.objects.get(id=document_id)
        document.parsing_status = 'In Progress'
        document.save(update_fields=['parsing_status'])

        # Read the file content
        file_content = document.file.read().decode('utf-8')

        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key="your_api_key_here")

        # Call Claude to parse the resume
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.2,
            system="You are an expert resume parser. Parse the given resume and structure the data according to the provided Django models.",
            messages=[
                {
                    "role": "user",
                    "content": f"Parse this resume and structure the data according to these Django models: PersonalInformation, Education, WorkExperience, Skill, Project, Certification. Here's the resume:\n\n{file_content}"
                }
            ]
        )

        # Process Claude's response
        parsed_data = eval(message.content)  # Be cautious with eval in production!

        # Save parsed data to database
        personal_info = PersonalInformation.objects.create(customer=document.customer, **parsed_data['personal_info'])

        for edu in parsed_data['education']:
            Education.objects.create(personal_info=personal_info, **edu)

        for exp in parsed_data['work_experience']:
            WorkExperience.objects.create(personal_info=personal_info, **exp)

        for skill in parsed_data['skills']:
            Skill.objects.create(personal_info=personal_info, **skill)

        for project in parsed_data['projects']:
            Project.objects.create(personal_info=personal_info, **project)

        for cert in parsed_data['certifications']:
            Certification.objects.create(personal_info=personal_info, **cert)

        # Save Claude's response
        ClaudeResponse.objects.create(
            response_id=message.id,
            response_type="resume_parsing",
            response_content_type="text",
            response_content_text=message.content,
            response_model=message.model,
            response_stop_reason=message.stop_reason,
            response_stop_sequence=message.stop_sequence or "",
            response_usage_input_tokens=message.usage.input_tokens,
            response_usage_output_tokens=message.usage.output_tokens
        )

        document.parsing_status = 'Success'
        document.save(update_fields=['parsing_status'])

    except Exception as e:
        document.parsing_status = 'Failed'
        document.save(update_fields=['parsing_status'])
        print(f"Parsing failed: {str(e)}")
