from rest_framework import serializers
from .models import Conversation, Message, ConversationEvent

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ConversationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationEvent
        fields = '__all__'
