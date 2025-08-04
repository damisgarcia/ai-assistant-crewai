from django.db import models
from django.conf import settings

class Contact(models.Model):
    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('cpf', 'CPF'),
        ('rg', 'RG'),
        ('cnh', 'CNH'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    birthdate = models.DateField(null=True, blank=True)
    document = models.CharField(max_length=20, null=True, blank=True)
    document_type = models.CharField(max_length=4, choices=DOCUMENT_TYPE_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')

    def __str__(self):
        return self.full_name
