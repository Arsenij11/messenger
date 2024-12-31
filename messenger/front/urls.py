from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^main_page/(?P<username>[A-Za-z]+)$', views.Main.as_view(), name='main page'),
    re_path(r'^create_profile$', views.ProfileCreate.as_view(), name='create_profile'),
    re_path(r'^update_profile/(?P<username>[A-Za-z]+)$', views.ProfileUpdate.as_view(), name='update_profile'),

    re_path(r'^allchats$', views.AllChats.as_view(), name='chats'),
    re_path(r'^chat/(?P<chat_id>[1-9]+)$', views.GroupPrivateChat.as_view(), name='chat'),
]