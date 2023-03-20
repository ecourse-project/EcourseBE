from django.urls import path
from apps.courses.api import views


urlpatterns = [
    path("", views.CourseListView.as_view()),
    path("most-download/", views.MostDownloadedCourseView.as_view()),
    path("my-courses/", views.UserCoursesListView.as_view()),
    path("detail/", views.CourseRetrieveView.as_view()),
    path("update-lesson-progress/", views.UpdateLessonProgress.as_view()),
    path("home/", views.HomepageCourseListAPIView.as_view()),
]
