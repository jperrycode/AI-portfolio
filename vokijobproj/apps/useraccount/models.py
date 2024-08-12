from django.db import models
import string
import random
from django.utils import timezone

class CustomerAccount(models.Model):
    user_f_name = models.CharField(max_length=100)
    user_l_name = models.CharField(max_length=100)
    user_account_id = models.CharField(max_length=20, unique=True)
    user_email = models.EmailField(unique=True)
    user_phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.user_account_id:
            self.user_account_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_f_name} {self.user_l_name}"

    def generate_unique_id(self):
        characters = string.ascii_lowercase + string.digits
        while True:
            new_id = ''.join(random.choice(characters) for _ in range(15))
            if not CustomerAccount.objects.filter(user_account_id=new_id).exists():
                return new_id


class CustomerMetadata(models.Model):
    customer = models.OneToOneField(CustomerAccount, on_delete=models.CASCADE, related_name='metadata')
    last_activity = models.DateTimeField(default=timezone.now)
    total_documents = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)

    def __str__(self):
        return f"Metadata for {self.customer}"

    def update_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

    def increment_documents(self):
        self.total_documents += 1
        self.save(update_fields=['total_documents'])

    def increment_submissions(self):
        self.total_submissions += 1
        self.save(update_fields=['total_submissions'])
