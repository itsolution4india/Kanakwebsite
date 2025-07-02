from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=100)
    subscribe_sms = models.BooleanField(default=False)
    subscribe_email = models.BooleanField(default=False)
    subscribe_voice = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name