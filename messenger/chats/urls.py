from django.urls import path, include, re_path

from . import views




urlpatterns = [
    path('new_message', views.NewMessageAPIView.as_view() ,name='new message'),
]