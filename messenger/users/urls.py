from django.urls import path, include, re_path

from users.views import AccountCreateAPI, AccountUpdateAPI, AccountDeleteAPI

urlpatterns = [
    path('drf-auth/', include('rest_framework.urls')),
    path('create', AccountCreateAPI.as_view()),
    path('update/<int:pk>', AccountUpdateAPI.as_view()),
    path('delete/<int:pk>', AccountDeleteAPI.as_view()),
    path('auth', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]