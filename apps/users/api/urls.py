from django.urls import path, include
from apps.users.api import views

urlpatterns = [
    path("user-info/", views.UserInfoView.as_view()),
    path("me/", views.UsersProfileView.as_view()),
    path("exists/", views.UserExistView.as_view(), name="user-exists"),
    path("password-reset/", views.PasswordResetView.as_view()),
    path("password-change/", views.ChangePasswordView.as_view()),
]
