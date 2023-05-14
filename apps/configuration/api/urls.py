from django.urls import path
from apps.configuration.api import views


urlpatterns = [
    path("payment-info/", views.PaymentInfoView.as_view()),
]