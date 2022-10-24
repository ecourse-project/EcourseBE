from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quiz.models import Quiz, Answer
from apps.quiz.api.serializers import QuizSerializer
from apps.quiz.exceptions import CompletedQuizException
from apps.courses.models import CourseManagement


class ListQuizView(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        return Quiz.objects.filter(course_id=course_id)


class QuizResultView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        course_id = data.get('course_id')
        user = self.request.user
        answers = data.get('answers')
        # if CourseManagement.objects.filter(user=user, course_id=course_id, is_done_quiz=True).first():
        #     raise CompletedQuizException

        user_answers_list = []
        correct_answers = 0

        for count, answer in enumerate(answers, start=0):
            quiz = Quiz.objects.filter(id=answer.get('quiz_id'), course_id=course_id).first()
            if answer.get('answer_choice') == quiz.correct_answer.choice:
                correct_answers += 1
            user_answers_list.append(Answer(choice=answer.get('answer_choice'), user=user, quiz=quiz))
            answers[count]['correct_answer'] = quiz.correct_answer.choice

        Answer.objects.bulk_create(user_answers_list)
        mark = round(10 * correct_answers / len(answers), 1)
        # CourseManagement.objects.filter(user=user, course_id=course_id).update(mark=mark, is_done_quiz=True)

        return Response(
            data={
                "mark": mark,
                "correct_answers": correct_answers,
                "total_quiz": len(answers),
                "quiz_answers": answers,
            },
            status=status.HTTP_200_OK,
        )
