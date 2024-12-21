from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from chats.models import Chat
from chats.permissions import IsOwnerOrReadOnly
from chats.serializers import ChatSerializer


# Create your views here.




class ChatAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = (IsAuthenticated, )

class ChatCreateAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = (IsAuthenticated, )

class ChatDeleteAPIView(generics.DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

class ChatUpdateAPIView(generics.UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
