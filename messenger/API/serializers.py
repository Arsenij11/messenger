from rest_framework import serializers

from .models import Chat, Message, Participants


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['chat', 'user', 'message']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['chat', 'user']

