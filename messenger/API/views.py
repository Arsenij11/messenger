import json

from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Chat, Message, Participants, Account
from .permissions import IsOwnerOrReadOnly, IsAdminOfChat
from .serializers import ChatSerializer, MessageSerializer, ParticipantSerializer
from rest_framework.authtoken.models import Token


# Create your views here.


class NewMessageAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not Chat.objects.filter(pk=self.kwargs['chat_id']).exists() or not Account.objects.filter(pk = self.kwargs['user_id']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данного пользователя/чата не существует'}, ensure_ascii=False))

        if not Participants.objects.filter(user_id = self.kwargs['user_id'], chat_id = self.kwargs['chat_id']).exists() and\
            Chat.objects.get(pk = self.kwargs['chat_id']).is_private is None:
            return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником данного чата'}, ensure_ascii=False))

        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is None:
            participant = Participants.objects.get(user_id = self.kwargs['user_id'], chat_id = self.kwargs['chat_id'])
            if request.auth.key != participant.user.user.auth_token.key:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником данного чата'}, ensure_ascii=False))
        else:
            chat = Chat.objects.get(pk = self.kwargs['chat_id'])
            if request.auth.key != chat.admin.user.auth_token.key and request.auth.key != chat.is_private.second_user.user.auth_token.key:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником данного чата'}, ensure_ascii=False))


        return self.create(request, *args, **kwargs)

class NewParticipantAPIView(generics.CreateAPIView):
    queryset = Participants.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.id != Token.objects.get(key = request.auth.key).user.id:
            return HttpResponse(json.dumps({'detail' : 'Доступ запрещён. Вы не являетесь администратором чата'}, ensure_ascii=False))

        if Participants.objects.filter(chat_id = self.kwargs['chat_id'], user_id = self.kwargs['user_id']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данный пользователь уже является участником чата'}, ensure_ascii=False))

        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is not None:
            return HttpResponse(json.dumps({'detail' : 'Данный чат является приватным'}, ensure_ascii=False))

        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        account = Participants.objects.create(chat_id=self.kwargs['chat_id'], user_id = self.kwargs['user_id'])
        return HttpResponse(json.dumps({
            'chat_id' : account.chat_id,
            'user_id' : account.user_id,
        }, ensure_ascii=False))

# class CreateChatAPIView(generics.CreateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = Chat
#     permission_classes = (IsAuthenticated,)

class DeleteChatAPIView(generics.DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is not None:
            if Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.id != Token.objects.get(key=request.auth.key).user.id\
                and Chat.objects.get(pk=self.kwargs['chat_id']).is_private.user.id != Token.objects.get(key=request.auth.key).user.id:
                    return HttpResponse(json.dumps({'detail' : 'Доступ запрещён. Вы не являетесь администратором чата'}, ensure_ascii=False))

        else:
            if Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.id != Token.objects.get(key=request.auth.key).user.id:
                return HttpResponse(json.dumps({'detail': 'Доступ запрещён. Вы не являетесь администратором чата'}, ensure_ascii=False))

        return self.destroy(request, *args, **kwargs)


class MessageListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        messages = Message.objects.filter(chat_id = self.kwargs['chat_id'])
        return messages

    def get(self, request, *args, **kwargs):
        if not Chat.objects.filter(pk=self.kwargs['chat_id']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данного чата не существует'}, ensure_ascii=False))

        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is None:
            user_ids = [p.user.user.id for p in Chat.objects.get(pk=self.kwargs['chat_id']).participants.all()]
            if request.auth.key not in [token.key for token in Token.objects.filter(user_id__in = user_ids)]:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником беседы'}, ensure_ascii=False))

        else:
            user_ids = [Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.pk, Chat.objects.get(pk=self.kwargs['chat_id']).is_private.second_user.user.pk]
            if request.auth.key not in [token.key for token in Token.objects.filter(user_id__in = user_ids)]:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником беседы'}, ensure_ascii=False))


        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        messages = [{'chat_id' : m.chat.id, 'name' :  m.user.name, 'message' : m.message, 'user_photo' :
                    m.user.profile_picture.url, 'username' : m.user.username, }
                    for m in Message.objects.filter(chat_id = self.kwargs['chat_id'])]

        return HttpResponse(json.dumps(messages, ensure_ascii=False))



