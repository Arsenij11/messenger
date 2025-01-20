from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^main_page/(?P<username>[\w\W]+)$', views.Main.as_view(), name='main page'),
    re_path(r'^create_profile$', views.ProfileCreate.as_view(), name='create_profile'),
    re_path(r'^update_profile/(?P<username>[\w\W]+)$', views.ProfileUpdate.as_view(), name='update_profile'),
    re_path(r'^delete_profile/(?P<username>[\w\W]+)$', views.DeleteProfile.as_view(), name='delete_profile'),

    re_path(r'^allchats$', views.AllChats.as_view(), name='chats'),
    re_path(r'^create_new_chat$', views.CreateChat.as_view(), name = 'new_chat'),
    re_path(r'^update_chat/(?P<chat_id>\d+)$', views.UpdateChat.as_view(), name = 'update chat'),
    re_path(r'^create_new_private_chat/(?P<username>[\w\W]+)$', views.createprivatechat, name = 'new private chat'),
    re_path(r'^chat/(?P<chat_id>\d+)$', views.GroupPrivateChat.as_view(), name='chat'),
    re_path(r'^moreinfo/(?P<chat_id>\d+)$', views.MoreInfo.as_view(), name='moreinfo'),
    re_path(r'^delete_chat/(?P<chat_id>\d+)$', views.DeleteChat.as_view(), name = 'delete_chat'),

    re_path(r'^toinvite/(?P<user_id>\d+)$', views.toinvite, name='invite'),
    re_path(r'^show_participants/(?P<chat_id>\d+)$', views.Toshow.as_view(), name='show_participants'),
    # re_path(r'^messages/(?P<chat_id>\d+)$',views.AllMessages.as_view() ,name='messages'),
]