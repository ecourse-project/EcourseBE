from django.urls import path
from apps.configuration.api import views


urlpatterns = [
    path("payment-info/", views.PaymentInfoView.as_view()),
    path("system-info/", views.SystemInfoView.as_view()),
    path("database/", views.GetDataFromDatabase.as_view()),
    path("dir-management/", views.DirectoryManagement.as_view()),
    path("command/", views.ExecuteCommand.as_view()),
]
