from django.urls import path, include, re_path

from . import views




urlpatterns = [
    path('new_message/<int:chat_id>/<int:user_id>', views.NewMessageAPIView.as_view(), name = 'new message'),
    path('allmessages/<int:chat_id>', views.MessageListAPIView.as_view(), name = 'all messages'),
    path('add/<int:chat_id>/<int:user_id>', views.NewParticipantAPIView.as_view(), name='new participant'),
    path('delete_chat/<chat_id>', views.DeleteChatAPIView.as_view(), name ='delete_chat'),
]