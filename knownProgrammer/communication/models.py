from django.db import models
from django.conf import settings


# Create your models here.

class Communicate(models.Model):
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_by_message')
    sent_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_to_message')
    contents = models.TextField(max_length=5000, null=False)
    title = models.CharField(max_length=100, null=False)