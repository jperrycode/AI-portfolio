# Generated by Django 5.0.7 on 2024-08-12 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileintake', '0003_remove_document_s3_key_document_upload_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='upload_status',
            new_name='parsing_status',
        ),
    ]
