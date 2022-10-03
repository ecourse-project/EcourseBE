from django.urls import path, include
from apps.payment.api import views

urlpatterns = [
    path("orders/", views.OrderListView.as_view()),
    path("order/create/", views.CreateOrderView.as_view()),
    path("order/detail/", views.OrderRetrieveView.as_view()),
    path("order/cancel/", views.CancelOrderView.as_view()),
]