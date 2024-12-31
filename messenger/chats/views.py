from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from chats.models import Chat, Message
from chats.permissions import IsOwnerOrReadOnly
from chats.serializers import ChatSerializer, MessageSerializer


# Create your views here.


class NewMessageAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)


