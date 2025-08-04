from django.db import models
from django.conf import settings

class Contact(models.Model):
    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')

    def __str__(self):
        return self.full_name
