from django.urls import path, include

from apps.settings.api import views

urlpatterns = [
    path("headers/", views.HeaderAPIView.as_view()),
]