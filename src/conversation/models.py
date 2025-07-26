from django.conf import settings
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.

class Conversation(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("expired", "Expired"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    title = models.CharField(max_length=255, blank=True, null=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    SENDER_TYPE_CHOICES = [
        ("user", "User"),
        ("ai_agent", "AI Agent"),
        ("agent", "Agent"),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPE_CHOICES)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ConversationEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ("user_registered", "User Registered"),
        ("transferred_to_agent", "Transferred to Agent"),
        ("conversation_closed", "Conversation Closed"),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=32, choices=EVENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(pre_save, sender=Conversation)
def set_closed_at_on_status_change(sender, instance, **kwargs):
    if instance.pk:
        orig = Conversation.objects.get(pk=instance.pk)
        if orig.status != instance.status and instance.status == "closed":
            instance.closed_at = timezone.now()

@receiver(post_save, sender=Conversation)
def set_expired_at_on_create(sender, instance, created, **kwargs):
    if created and not instance.expired_at:
        instance.expired_at = instance.created_at + timedelta(hours=1)
        instance.save(update_fields=["expired_at"])
