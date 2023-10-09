from django.db.models import Prefetch
from django.http import FileResponse

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quiz.models import (
    ChoicesQuizAnswer,
    QuizManagement,
    MatchColumnContent,
)
from apps.quiz.api.serializers import QuizManagementSerializer
from apps.quiz.exceptions import CompletedQuizException
from apps.quiz.services.services import (
    store_user_answers,
    quiz_statistic,
)
from apps.courses.models import CourseManagement, Course
from apps.courses.exceptions import NoItemException

from reportlab.lib.units import inch, toLength
from apps.quiz.services.certificate_services import insert_text_to_pdf
from apps.quiz.certificate.templates import add_info_certificate, certificate_form


class ListQuizView(generics.ListAPIView):
    serializer_class = QuizManagementSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        if not course_id:
            raise NoItemException("Missing course ID")
        return QuizManagement.objects.select_related(
            "course",
            "choices_question",
            "match_question",
        ).prefetch_related(
            Prefetch(
                "match_question__first_column",
                queryset=MatchColumnContent.objects.select_related("content_image")
            ),
            Prefetch(
                "match_question__second_column",
                queryset=MatchColumnContent.objects.select_related("content_image")
            ),
            Prefetch(
                "choices_question__choices",
                queryset=ChoicesQuizAnswer.objects.select_related("answer_image", "choice_name")
            ),
        ).filter(course_id=course_id)


class QuizResultView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        course_id = data.get('course_id')
        user = self.request.user
        answers = data.get('user_answers')
        if CourseManagement.objects.filter(user=user, course_id=course_id, is_done_quiz=True).first():
            raise CompletedQuizException
        store_user_answers(user=user, user_answers=answers)
        return Response(
            data=quiz_statistic(user=user, course_id=course_id),
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
