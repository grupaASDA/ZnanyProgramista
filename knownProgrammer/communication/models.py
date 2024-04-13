from django.db import models
from django.conf import settings


# Create your models here.

class Message(models.Model):
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_by_message')
    sent_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_to_message')
    content = models.TextField(max_length=5000, null=False)
    title = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

