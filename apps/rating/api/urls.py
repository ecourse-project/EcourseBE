from django.urls import path, include

from apps.rating.api import views

urlpatterns = [
    path("document/rate/", views.DocumentRateAPIView.as_view()),
    path("course/rate/", views.CourseRateAPIView.as_view()),
    path("document/rating/list/", views.DocumentListRate.as_view()),
    path("course/rating/list/", views.CourseListRate.as_view()),
]