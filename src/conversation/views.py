from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from .models import Conversation, Message, ConversationEvent
from .serializers import ConversationSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = None  # Será definido no __init__

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_pk"]
        return Message.objects.filter(conversation_id=conversation_id)

    def get_serializer_class(self):
        from .serializers import MessageSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        conversation_id = self.kwargs["conversation_pk"]
        serializer.save(conversation_id=conversation_id)

class ConversationEventViewSet(viewsets.ModelViewSet):
    serializer_class = None  # Será definido no __init__

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_pk"]
        return ConversationEvent.objects.filter(conversation_id=conversation_id)

    def get_serializer_class(self):
        from .serializers import ConversationEventSerializer
        return ConversationEventSerializer

    def perform_create(self, serializer):
        conversation_id = self.kwargs["conversation_pk"]
        serializer.save(conversation_id=conversation_id)
