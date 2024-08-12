from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import CustomerMetadata
from apps.fileintake.models import Document, DocumentSubmission

@receiver(post_save, sender=Document)
def update_metadata_on_document_upload(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            metadata, _ = CustomerMetadata.objects.get_or_create(customer=instance.customer)
            metadata.update_activity()
            metadata.increment_documents()

@receiver(post_save, sender=DocumentSubmission)
def update_metadata_on_submission(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            metadata, _ = CustomerMetadata.objects.get_or_create(customer=instance.customer)
            metadata.update_activity()
            metadata.increment_submissions()