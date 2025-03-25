from django.shortcuts import get_object_or_404
from rest_framework import permissions
# from rest_framework.generics import get_object_or_404

from .models import Chat


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.admin.user == request.user

class IsAdminOfChat(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.admin.id == request.user.account.id

# class IsAdminOfChatToInvite(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         return Chat.objects.get(pk=self.kwargs['chat_id']).admin.id == request.user.account.id