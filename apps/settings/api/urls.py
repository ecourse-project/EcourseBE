from django.urls import path, include

from apps.settings.api import views

urlpatterns = [
    path("headers/", views.HeaderAPIView.as_view()),
    path("home/", views.HomePageAPIView.as_view()),
    path("init/", views.InitData.as_view()),
    path("search/", views.SearchItem.as_view()),
]