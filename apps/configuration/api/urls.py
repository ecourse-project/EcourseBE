from django.urls import path
from apps.configuration.api import views


urlpatterns = [
    path("search/", views.SearchItemView.as_view()),
    path("payment-info/", views.PaymentInfoView.as_view()),
]
