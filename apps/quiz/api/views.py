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
            if answer.get('answer_choice') == quiz.correct_answer.choice:
                correct_answers += 1
            user_answers_list.append(Answer(choice=answer.get('answer_choice'), user=user, quiz=quiz))
            answers[count]['correct_answer'] = quiz.correct_answer.choice

        Answer.objects.bulk_create(user_answers_list)
        mark = round(10 * correct_answers / len(answers), 1)
        CourseManagement.objects.filter(user=user, course_id=course_id).update(mark=mark, is_done_quiz=True)

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
        # response = HttpResponse(content_type="application/pdf", status=status.HTTP_201_CREATED)
        # response["Content-Disposition"] = "attachment;filename=certificate.pdf"

        # 17 in = 1224, 11 in = 792
        # presented to (size 23, 380, 450, left, color (0.4, 0.4, 0.4))
        # name (size 35, 500, 450, left, color (0.2, 0.2, 0.2))
        # has successfully completed (size 23, 380, 410, left, color(0.4, 0.4, 0.4))
        # course (size 25, 615, 410, left, color(0.2, 0.2, 0.2)
        output_stream = insert_text_to_pdf(
            x=615,
            y=410,
            font_path="templates/font/Charm-Bold.ttf",
            text="Cơ Sở Dữ Liệu",
            size=25,
            color=(0.2, 0.2, 0.2),
            input_pdf="templates/certificate/certi5.pdf",
            pagesize=(17 * inch, 11 * inch),
        )


        # pagesize = (266 * mm, 150 * mm)  # (1057.3228346456694, 595.2755905511812)
        # my_canvas = canvas.Canvas(response, pagesize=pagesize)
        # my_canvas.drawImage('templates/certificate/certificate.png', 0, 0, width=754, height=425)
        #
        # course_id = self.request.query_params.get("course_id")
        # # course_name = Course.objects.filter(id=course_id).first().name or "NONE"
        # # user_name = self.request.user.full_name or "NONE"
        # user_name = "DHB"
        # course_name="HAHA"
        #
        # # text_width = stringWidth(text, fontName="Helvetica", fontSize=30)
        # # my_canvas.setFont("Helvetica-Bold", 40, leading=None)
        # # my_canvas.setFillColor()
        # my_canvas.setFont("Helvetica", 35, leading=None)
        # my_canvas.drawCentredString(458, 220, text=user_name)
        # my_canvas.setFont("Helvetica", 12, leading=None)
        # my_canvas.drawCentredString(458, 150, text=course_name)
        # my_canvas.save()

        response = FileResponse(output_stream, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="merged_output.pdf"'

        return response
