from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Conversation
from .serializers import ConversationSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
