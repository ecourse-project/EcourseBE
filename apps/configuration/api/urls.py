from django.urls import path
from apps.configuration.api import views


urlpatterns = [
    path("personal-info/", views.PersonalInfoView.as_view()),
]