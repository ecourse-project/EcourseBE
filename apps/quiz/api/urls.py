from django.urls import path, include

from apps.quiz.api import views

urlpatterns = [
    path("result/", views.QuizResultView.as_view()),
    path("certi/", views.GenerateCertificate.as_view()),
    path("start-time/", views.QuizStartTimeView.as_view()),
    path("assign/", views.QuizAssignment.as_view()),
    path("question/delete/", views.DeleteQuestionView.as_view()),
    path("question/", views.QuestionView.as_view()),
    path("delete/", views.DeleteQuizView.as_view()),
    path("", views.QuizView.as_view()),
]