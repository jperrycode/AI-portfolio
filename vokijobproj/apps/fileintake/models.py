from django.db import models
from django.core.files.storage import default_storage
from apps.useraccount.models import CustomerAccount
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models
from django.core.files.storage import default_storage
from apps.useraccount.models import CustomerAccount
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.aistream.tasks import parse_resume_task  # Adjust the import path as needed

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('RESUME', 'Resume'),
        ('COVER_LETTER', 'Cover Letter'),
    ]
    customer = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=12, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/', storage=default_storage)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsing_status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.file_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.parsing_status = 'Pending'
        super().save(*args, **kwargs)

        if self.parsing_status == 'Pending' and self.file:
            self.parsing_status = 'Success'
            self.save(update_fields=['parsing_status'])

            DocumentSubmission.objects.update_or_create(
                document=self,
                defaults={'status': 'Success'}
            )

@receiver(post_save, sender=Document)
def trigger_resume_parsing(sender, instance, created, **kwargs):
    if instance.document_type == 'RESUME' and instance.parsing_status == 'Success':
        parse_resume_task.delay(instance.id)

class DocumentSubmission(models.Model):
    customer = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, related_name='submissions')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Submission for {self.customer.user.username} - {self.document.file_name} at {self.submitted_at}"

