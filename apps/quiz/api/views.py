import datetime

from reportlab.lib.units import inch, toLength
from django.http import FileResponse
from django.db.models import Prefetch

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.quiz.api.serializers import (
    QuestionManagementSerializer,
    QuizSerializer,
)
from apps.quiz.services.services import (
    add_quiz,
    delete_quiz,
    assign_quiz,
    store_question,
    delete_question,
    store_user_answers,
    quiz_statistic,
    response_quiz_statistic,
)
from apps.quiz.services.queryset_services import get_question_queryset
from apps.quiz.services.certificate_services import insert_text_to_pdf
from apps.quiz.certificate.templates import add_info_certificate
from apps.quiz.models import Quiz
from apps.courses.models import CourseManagement, QuizManagement, Course
from apps.core.utils import get_now
from apps.users_auth.authentication import QuizPermission


class QuizAssignment(APIView):
    permission_classes = (QuizPermission,)

    def post(self, request, *args, **kwargs):
        assign_quiz(request.data)
        return Response(data={})


class QuizView(APIView):
    permission_classes = (QuizPermission,)

    def get(self, request, *args, **kwargs):
        list_quiz = Quiz.objects.prefetch_related(
            Prefetch("question_mngt", queryset=get_question_queryset())
        ).filter(author=self.request.user)
        return Response(data=QuizSerializer(list_quiz, many=True).data)

    def post(self, request, *args, **kwargs):
        quiz = add_quiz(request.data, request.user)
        return Response(data=QuizSerializer(quiz).data)


class DeleteQuizView(APIView):
    permission_classes = (QuizPermission,)

    def get(self, request, *args, **kwargs):
        delete_quiz(self.request.query_params.get("quiz_id"))
        return Response(data={})


class QuestionView(APIView):
    permission_classes = (QuizPermission,)

    def get(self, request, *args, **kwargs):
        qs = get_question_queryset().order_by("order")
        return Response(data=QuestionManagementSerializer(qs, many=True).data)

    def patch(self, request, *args, **kwargs):
        quiz_id = request.data.get("quiz_id")
        question_data = request.data.get("question")
        old_question_id = question_data.pop("id")
        new_question = store_question([question_data])
        quiz = Quiz.objects.get(pk=quiz_id)
        if new_question and isinstance(new_question, list):
            quiz.question_mngt.add(new_question[0])
            delete_question(old_question_id)
        return Response(data=QuizSerializer(quiz).data)

    def post(self, request, *args, **kwargs):
        quiz_id = request.data.get("quiz_id")
        question = store_question([request.data.get("question")], request.user)
        quiz = Quiz.objects.get(pk=quiz_id)
        if question and isinstance(question, list):
            quiz.question_mngt.add(question[0])
        return Response(data=QuizSerializer(quiz).data)


class DeleteQuestionView(APIView):
    permission_classes = (QuizPermission,)

    def post(self, request, *args, **kwargs):
        delete_question(request.data)  # list_id
        return Response(data={})


class QuizResultView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user = self.request.user
        answers = data.get('user_answers')
        quiz_id = data.get('id')
        course_id = data.get('course_id')
        lesson_id = data.get('lesson_id')

        created, _, _, _ = store_user_answers(user=user, user_answers=answers)
        user_quiz_info = quiz_statistic(quiz_id=quiz_id, user=user, created=created)
        quiz_mngt, _ = QuizManagement.objects.get_or_create(
            course_id=course_id, lesson_id=lesson_id, quiz_id=quiz_id, user=user
        )
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
        quiz_id = self.request.query_params.get('quiz_id')
        is_start = self.request.query_params.get('is_start', '').lower() == "true"
        res = None

        quiz_mngt, _ = QuizManagement.objects.get_or_create(
            course_id=course_id, lesson_id=lesson_id, quiz_id=quiz_id, user=request.user
        )
        if is_start:
            if quiz_mngt.start_time:
                res = quiz_mngt.start_time
            else:
                res = get_now()
                quiz_mngt.start_time = res
                quiz_mngt.save(update_fields=["start_time"])
        else:
            res = quiz_mngt.start_time if quiz_mngt.start_time else res

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
