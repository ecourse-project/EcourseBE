from django.urls import path
from apps.classes.api import views
from apps.courses.api.views import UpdateLessonProgress


urlpatterns = [
    path("", views.ClassListView.as_view()),
    path("join-request/", views.JoinRequestView.as_view()),
    path("detail/", views.ClassDetailView.as_view()),
    path("home/", views.HomepageClassListAPIView.as_view()),
    path("update-lesson-progress/", UpdateLessonProgress.as_view()),
]
