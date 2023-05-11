from django.urls import path

from apps.posts.api import views


urlpatterns = [
    path("", views.PostListView.as_view()),
    path("detail/", views.PostRetrieveView.as_view()),
]
