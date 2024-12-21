from django.urls import path, include, re_path

from . import views




urlpatterns = [
    path('', views.ChatAPIView.as_view()),
    path('api/chat/update/<int:pk>', views.ChatUpdateAPIView.as_view()),
    path('api/chat/delete/<int:pk>', views.ChatDeleteAPIView.as_view()),

]