from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField  # For Django 1.8.3

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class EmailLog(models.Model):
    to_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=50)
    sent_at = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(EmailTemplate, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.to_email} - {self.subject}"

class UserEmailSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_frequency = models.CharField(max_length=50, default='daily')
    notification_types = models.TextField(default='[]')  # Stored as JSON string
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s email settings"

class EmailMetadata(models.Model):
    email = models.ForeignKey(EmailLog, on_delete=models.CASCADE)
    metadata = JSONField(default=dict)  # Stores email metadata as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Metadata for {self.email.subject}" 