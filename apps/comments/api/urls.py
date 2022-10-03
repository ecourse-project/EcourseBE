from django.urls import path, include
from apps.comments.api import views

urlpatterns = [
    path("create/", views.CreateCommentView.as_view()),
    path("list/", views.ListAllCommentsView.as_view()),
]
