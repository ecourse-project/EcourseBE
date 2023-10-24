from django.urls import path, include

from apps.quiz.api import views

urlpatterns = [
    path("create/", views.CreateQuizView.as_view()),
    path("result/", views.QuizResultView.as_view()),
    path("certi/", views.GenerateCertificate.as_view()),
    path("start-time/", views.QuizStartTimeView.as_view()),
    path("", views.ListQuizView.as_view()),
]