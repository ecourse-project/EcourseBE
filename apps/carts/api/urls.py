from django.urls import path, include
from apps.carts.api import views

urlpatterns = [
    path("info/", views.CartInfoAPIView.as_view()),
    path("favorite/info/", views.FavoriteListInfoAPIView.as_view()),
    path("document/move/", views.MoveDocument.as_view()),
    path("course/move/", views.MoveCourse.as_view()),
]
