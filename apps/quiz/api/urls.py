from django.urls import path, include

from apps.quiz.api import views

urlpatterns = [
    path("result/", views.QuizResultView.as_view()),
    path("certi/", views.GenerateCertificate.as_view()),
    path("start-time/", views.QuizStartTimeView.as_view()),
    path("", views.QuizView.as_view()),
]