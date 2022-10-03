from django.urls import path, include
from apps.upload.api import views

urlpatterns = [
    path("upload-files/", views.UploadFileView.as_view()),
    path("upload-images/", views.UploadImageView.as_view()),
]