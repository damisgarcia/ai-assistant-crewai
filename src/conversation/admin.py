from django.contrib import admin
from .models import Conversation, Message, ConversationEvent

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ConversationEvent)
