from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView

from chats.models import Account
from users.serializers import AccountSerializer


# Create your views here.

class AccountCreateAPI(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountUpdateAPI(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDeleteAPI(DestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer