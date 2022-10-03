from django.urls import path, include
from apps.carts.api import views

urlpatterns = [
    path("info/", views.CartInfoAPIView.as_view()),
    path("favorite/info/", views.FavoriteListInfoAPIView.as_view()),
    path("move/", views.MoveItemsAPIView.as_view()),
]
