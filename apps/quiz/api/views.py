import datetime

from reportlab.lib.units import inch, toLength
from django.http import FileResponse

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quiz.api.serializers import QuizManagementSerializer
from apps.quiz.exceptions import CompletedQuizException
from apps.quiz.services.services import (
    store_quiz,
    delete_quiz,
    edit_quiz,
    store_user_answers,
    quiz_statistic,
    response_quiz_statistic,
    validate_lesson_of_course,
)
from apps.quiz.services.queryset_services import get_quiz_queryset
from apps.quiz.services.certificate_services import insert_text_to_pdf
from apps.quiz.certificate.templates import add_info_certificate
from apps.courses.models import CourseManagement, LessonManagement, LessonQuizManagement, Course
from apps.courses.exceptions import NoItemException
from apps.core.utils import get_now
from apps.users_auth.authentication import ManagerPermission


class QuizView(APIView):
    permission_classes = (ManagerPermission,)

    def get(self, request, *args, **kwargs):
        course_id = self.request.query_params.get("course_id")
        lesson_id = self.request.query_params.get("lesson_id")
        if not course_id:
            raise NoItemException("Missing course ID")
        if not lesson_id:
            raise NoItemException("Missing lesson ID")
        qs = get_quiz_queryset().filter(course_id=course_id, lesson_id=lesson_id).order_by("order")
        return Response(data=QuizManagementSerializer(qs, many=True).data)

    def patch(self, request, *args, **kwargs):
        new_quiz = edit_quiz(request.data)
        return Response(data=QuizManagementSerializer(new_quiz, many=True).data)

    def post(self, request, *args, **kwargs):
        quiz = store_quiz(request.data)
        return Response(data=QuizManagementSerializer(quiz, many=True).data)

    def delete(self, request, *args, **kwargs):
        delete_quiz(request.data)
        return Response(data={})


class QuizResultView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        course_id = data.get('course_id')
        lesson_id = data.get('lesson_id')
        user = self.request.user
        answers = data.get('user_answers')
        if not course_id or not lesson_id:
            raise NoItemException("Missing lesson ID or course ID")
        course_mngt = CourseManagement.objects.filter(user=user, course_id=course_id).first()
        if (
            not course_mngt or not LessonManagement.objects.filter(course_id=course_id, lesson_id=lesson_id)
        ):
            raise NoItemException("Lesson does not exist or Lesson does not belong to the course")
        if LessonQuizManagement.objects.filter(course_mngt=course_mngt, lesson_id=lesson_id, is_done_quiz=True):
            raise CompletedQuizException

        created, _, _, _ = store_user_answers(user=user, user_answers=answers)
        user_quiz_info = quiz_statistic(user=user, course_id=course_id, lesson_id=lesson_id, created=created)
        quiz_mngt, _ = LessonQuizManagement.objects.get_or_create(course_mngt=course_mngt, lesson_id=lesson_id)
        quiz_mngt.is_done_quiz = True
        quiz_mngt.date_done_quiz = created
        quiz_mngt.save(update_fields=["is_done_quiz", "date_done_quiz"])

        return Response(
            data=response_quiz_statistic(user_quiz_info),
            status=status.HTTP_200_OK,
        )


class QuizStartTimeView(APIView):
    def get(self, request, *args, **kwargs):
        course_id = self.request.query_params.get('course_id')
        lesson_id = self.request.query_params.get('lesson_id')
        is_start = self.request.query_params.get('is_start', '').lower() == "true"
        res = None

        course_mngt = validate_lesson_of_course(self.request.user, lesson_id, course_id)
        if not course_mngt:
            raise NoItemException("Lesson does not exist or Lesson does not belong to the course")

        lesson_quiz_mngt, _ = LessonQuizManagement.objects.get_or_create(course_mngt=course_mngt, lesson_id=lesson_id)
        if is_start:
            if lesson_quiz_mngt.start_time:
                res = lesson_quiz_mngt.start_time
            else:
                res = get_now()
                lesson_quiz_mngt.start_time = res
                lesson_quiz_mngt.save(update_fields=["start_time"])
        else:
            res = lesson_quiz_mngt.start_time if lesson_quiz_mngt.start_time else res

        return Response(data={"start_time": res.isoformat() if isinstance(res, datetime.datetime) else None})


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
