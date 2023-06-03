import datetime

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quiz.models import Quiz, Answer
from apps.quiz.api.serializers import QuizSerializer
from apps.quiz.exceptions import CompletedQuizException
from apps.courses.models import CourseManagement, Course

from django.http import FileResponse
from reportlab.lib.units import inch, toLength
from apps.quiz.services.certificate_services import insert_text_to_pdf
from apps.quiz.certificate.templates import add_info_certificate, certificate_form


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
        if CourseManagement.objects.filter(user=user, course_id=course_id, is_done_quiz=True).first():
            raise CompletedQuizException

        user_answers_list = []
        correct_answers = 0

        for count, answer in enumerate(answers, start=0):
            quiz = Quiz.objects.filter(id=answer.get('quiz_id'), course_id=course_id).first()
            if not quiz:
                continue
            if answer.get('answer_choice') == quiz.correct_answer.choice:
                correct_answers += 1
            user_answers_list.append(Answer(choice=answer.get('answer_choice'), user=user, quiz=quiz))
            answers[count]['correct_answer'] = quiz.correct_answer.choice

        Answer.objects.bulk_create(user_answers_list)
        mark = round(10 * correct_answers / len(answers), 1)
        CourseManagement.objects.filter(user=user, course_id=course_id).update(
            mark=mark, is_done_quiz=True, date_done_quiz=datetime.datetime.now()
        )

        return Response(
            data={
                "mark": mark,
                "correct_answers": correct_answers,
                "total_quiz": len(answers),
                "quiz_answers": answers,
            },
            status=status.HTTP_200_OK,
        )


class GenerateCertificate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        course_id = self.request.query_params.get("course_id")
        course = Course.objects.filter(id=course_id).first()
        course_mngt = CourseManagement.objects.filter(course_id=course_id, user=self.request.user).first()

        username = self.request.user.full_name or ""
        course_name = course.name if course else ""
        date = ""
        if course_mngt:
            date_complete = course_mngt.date_done_quiz
            date = str(date_complete.date()) if date_complete else date

        output_stream = insert_text_to_pdf(
            attrs=add_info_certificate(username, course_name, date),
            input_pdf="templates/certificate/certificate_template.pdf",
            pagesize=(17 * inch, 11 * inch),
        )

        # Init template
        # output_stream = insert_text_to_pdf(
        #     attrs=certificate_form,
        #     input_pdf="templates/certificate/base.pdf",
        #     pagesize=(17 * inch, 11 * inch),
        # )

        response = FileResponse(output_stream, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=certificate.pdf'

        return response
