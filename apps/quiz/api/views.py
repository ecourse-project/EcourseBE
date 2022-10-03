from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quiz.models import Quiz
from apps.quiz.api.serializers import QuizSerializer


class ListQuizView(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        return Quiz.objects.filter(course_id=course_id).order_by('question_number')
