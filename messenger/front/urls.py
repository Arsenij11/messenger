from django.urls import path
from . import views

urlpatterns = [
    path('main_page/<int:pk>', views.main),
    path('create_profile', views.profile_create),
    # path('update_profile/<int:account_id>', views.ProfileUpdate.as_view()),
]