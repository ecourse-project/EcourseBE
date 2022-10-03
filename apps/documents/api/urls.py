from django.urls import path, include
from apps.documents.api import views

urlpatterns = [
    path("", views.DocumentListView.as_view()),
    path("most-download/", views.MostDownloadedDocumentView.as_view()),
    path("create/", views.DocumentCreateView.as_view()),
    path("detail/", views.DocumentRetrieveView.as_view()),
    path("my-documents/", views.UserDocumentsListView.as_view()),
]
