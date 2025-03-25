import json

from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Chat, Message, Participants, Account
from .permissions import IsOwnerOrReadOnly, IsAdminOfChat
from .serializers import ChatSerializer, MessageSerializer, ParticipantSerializer
from rest_framework.authtoken.models import Token


# Create your views here.


class NewMessageAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not Chat.objects.filter(pk=self.kwargs['chat_id']).exists() or not Account.objects.filter(pk = self.kwargs['user_id']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данного пользователя/чата не существует'},
                                           ensure_ascii=False), status = 404)

        if not Participants.objects.filter(user_id = self.kwargs['user_id'], chat_id = self.kwargs['chat_id']).exists() and\
            Chat.objects.get(pk = self.kwargs['chat_id']).is_private is None:
            return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником данного чата'},
                                           ensure_ascii=False), status = 403)

        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is None:
            participant = Participants.objects.get(user_id = self.kwargs['user_id'], chat_id = self.kwargs['chat_id'])
            if request.auth.key != participant.user.user.auth_token.key:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником данного чата'},
                                               ensure_ascii=False), status=403)
        else:
            chat = Chat.objects.get(pk = self.kwargs['chat_id'])
            if request.auth.key != chat.admin.user.auth_token.key and request.auth.key != chat.is_private.second_user.user.auth_token.key:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником данного чата'},
                                               ensure_ascii=False), status = 403)


        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        new_message = Message.objects.create(chat_id = self.kwargs['chat_id'],
                                             user_id = self.kwargs['user_id'],
                                             message = dict(request.data)['message'])
        message = {
                    'id' : new_message.id,
                    'user' : new_message.user.username,
                    'message' : new_message.message
                  }
        return HttpResponse(json.dumps(message, ensure_ascii=False), status=201)

class NewParticipantAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.id != Token.objects.get(key = request.auth.key).user.id:
            return HttpResponse(json.dumps({'detail' : 'Доступ запрещён. Вы не являетесь администратором чата'},
                                           ensure_ascii=False), status = 403)

        if Participants.objects.filter(chat_id = self.kwargs['chat_id'], user_id = self.kwargs['user_id']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данный пользователь уже является участником чата'},
                                           ensure_ascii=False), status = 400)

        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is not None:
            return HttpResponse(json.dumps({'detail' : 'Данный чат является приватным'}, ensure_ascii=False),
                                status=400)

        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        account = Participants.objects.create(chat_id=self.kwargs['chat_id'], user_id = self.kwargs['user_id'])
        return HttpResponse(json.dumps({
            'chat_id' : account.chat_id,
            'user_id' : account.user_id,
        }, ensure_ascii=False), status=201)

# class CreateChatAPIView(generics.CreateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = Chat
#     permission_classes = (IsAuthenticated,)

class DeleteChatAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(Chat, pk=self.kwargs['chat_id'])

    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps({'detail' : 'Метод GET не разрешён'}, ensure_ascii=False))

    def delete(self, request, *args, **kwargs):
        if not Chat.objects.filter(pk = self.kwargs['chat_id']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данного чата не существует'}, ensure_ascii=False))
        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is not None:
            if Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.id != Token.objects.get(key=request.auth.key).user.id\
                and Chat.objects.get(pk=self.kwargs['chat_id']).is_private.user.id != Token.objects.get(key=request.auth.key).user.id:
                    return HttpResponse(json.dumps({'detail' : 'Доступ запрещён. Вы не являетесь администратором чата'}, ensure_ascii=False), status=403)

        else:
            if Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.id != Token.objects.get(key=request.auth.key).user.id:
                return HttpResponse(json.dumps({'detail': 'Доступ запрещён. Вы не являетесь администратором чата'}, ensure_ascii=False), status = 403)

        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = {
            'id' : instance.id,
            'name' : instance.name,
            'about' : instance.about
        }
        self.perform_destroy(instance)
        return HttpResponse(json.dumps(response, ensure_ascii=False))


class MessageListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        messages = Message.objects.filter(chat_id = self.kwargs['chat_id'])
        return messages

    def get(self, request, *args, **kwargs):
        if not Chat.objects.filter(pk=self.kwargs['chat_id']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данного чата не существует'}, ensure_ascii=False), status=404)

        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is None:
            user_ids = [p.user.user.id for p in Chat.objects.get(pk=self.kwargs['chat_id']).participants.all()]
            if request.auth.key not in [token.key for token in Token.objects.filter(user_id__in = user_ids)]:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником беседы'}, ensure_ascii=False), status=403)

        else:
            user_ids = [Chat.objects.get(pk=self.kwargs['chat_id']).admin.user.pk, Chat.objects.get(pk=self.kwargs['chat_id']).is_private.second_user.user.pk]
            if request.auth.key not in [token.key for token in Token.objects.filter(user_id__in = user_ids)]:
                return HttpResponse(json.dumps({'detail' : 'Вы не являетесь участником беседы'}, ensure_ascii=False), status=403)


        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        messages = [{'id' : m.id,'chat_id' : m.chat.id, 'name' :  m.user.name, 'message' : m.message, 'user_photo' :
                    m.user.profile_picture.url, 'username' : m.user.username, }
                    for m in Message.objects.filter(chat_id = self.kwargs['chat_id'])]

        return HttpResponse(json.dumps(messages, ensure_ascii=False), status=200)


class DeleteMessageAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(Message, pk=self.kwargs['mes_id'])

    def get(self, request, *args, **kwargs):
        return HttpResponse(
                json.dumps({'detail': 'Метод GET недоступен'}, ensure_ascii=False),
                status=403,
            )


    def delete(self, request, *args, **kwargs):
        # Проверяем, существует ли сообщение
        if not Message.objects.filter(pk=self.kwargs['mes_id']).exists():
            return HttpResponse(
                json.dumps({'detail': 'Такого сообщения не существует'}, ensure_ascii=False),
                status=404,
            )

        # Проверяем наличие токена
        if not request.auth or not hasattr(request.auth, 'key'):
            return HttpResponse(
                json.dumps({'detail': 'Токен отсутствует или некорректен'}, ensure_ascii=False),
                status=401,
            )

        # Проверяем, является ли пользователь автором сообщения
        message = Message.objects.get(pk=self.kwargs['mes_id'])
        if message.user.user.id != Token.objects.get(key=request.auth.key).user.id:
            return HttpResponse(
                json.dumps({'detail': 'Вы не являетесь автором сообщения'}, ensure_ascii=False),
                status=403,
            )

        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = {
            'chat': instance.chat.id,
            'user': instance.user.id,
            'message': instance.message,
            'send_time': instance.send_time.isoformat(),
        }
        self.perform_destroy(instance)
        return HttpResponse(json.dumps(response, ensure_ascii=False))

class DeleteProfileAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(Account, username = self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps({'detail' : 'Метод GET не разрешён'}, ensure_ascii=False), status=400)

    def delete(self, request, *args, **kwargs):
        if not Account.objects.filter(username = self.kwargs['username']).exists():
            return HttpResponse(json.dumps({'detail' : 'Данного аккаунта не существует'}, ensure_ascii=False), status=404)
        elif Account.objects.get(username = self.kwargs['username']).user.auth_token.key != request.auth.key:
            return HttpResponse(json.dumps({'detail' : 'Вы не являетесь владельцем аккаунта'}, ensure_ascii=False), status=403)

        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = {
            'username': instance.username,
            'name': instance.name
        }
        self.perform_destroy(instance)
        return HttpResponse(json.dumps(response, ensure_ascii=False))

