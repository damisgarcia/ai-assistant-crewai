from django.db import models

# Create your models here.

class Conversation(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("expired", "Expired"),
    ]
    user = models.ForeignKey('django_app.User', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    open = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    SENDER_TYPE_CHOICES = [
        ("user", "User"),
        ("ai_agent", "AI Agent"),
        ("agent", "Agent"),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPE_CHOICES)
    sender_id = models.IntegerField(null=True, blank=True)
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
