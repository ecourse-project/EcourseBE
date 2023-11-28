from django.urls import path
from apps.system.api import views

urlpatterns = [
    path("system-info/", views.SystemInfoView.as_view()),
    path("storage/", views.StorageView.as_view()),
    path("database/", views.GetDataFromDatabase.as_view()),
    path("dir-management/", views.DirectoryManagement.as_view()),
    path("command/", views.ExecuteCommand.as_view()),
]
