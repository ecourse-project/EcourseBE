from django.urls import path
from apps.classes.api import views


urlpatterns = [
    path("join-request/", views.JoinRequestView.as_view()),
    path("detail/", views.ClassDetailView.as_view()),
    path("", views.ClassListView.as_view()),
]
