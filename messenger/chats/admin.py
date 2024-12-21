from django.contrib import admin

from chats.models import Account, Chat, Message

# Register your models here.

admin.site.register(Account)
admin.site.register(Chat)
admin.site.register(Message)