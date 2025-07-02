from django.db import models
from django.utils import timezone

class User(models.Model):
    SERVICE_CHOICES = [
        ('Real Estate', 'Real Estate'),
        ('Ayurveda', 'Ayurveda'),
        ('Credit Cards', 'Credit Cards'),
        ('Banking', 'Banking'),
        ('Finance', 'Finance'),
        ('Insurance', 'Insurance'),
        ('E-commerce', 'E-commerce'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Travel', 'Travel'),
        ('Telecom', 'Telecom'),
        ('Investment', 'Investment'),
        ('Stock Market', 'Stock Market'),
        ('Mutual Funds', 'Mutual Funds'),
        ('Loans', 'Loans'),
        ('Home Loans', 'Home Loans'),
        ('Mortgage', 'Mortgage'),
        ('Wealth Management', 'Wealth Management'),
    ]

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    location = models.CharField(max_length=100)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, null=True, blank=True)

    subscribe_sms = models.BooleanField(default=False)
    subscribe_email = models.BooleanField(default=False)
    subscribe_voice = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name