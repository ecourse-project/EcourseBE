from rest_framework import serializers

from apps.courses.models import CourseDocumentManagement, VideoManagement
from apps.courses.api.serializers import LessonSerializer, TopicSerializer, CourseSerializer, CourseManagementSerializer
from apps.classes.models import Class, ClassManagement
from apps.classes.services.services import ClassRequestService
from apps.quiz.models import Answer


class ClassSerializer(CourseSerializer):
    request_status = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)
    topic = TopicSerializer()

    class Meta(CourseSerializer.Meta):
        model = Class
        fields = CourseManagementSerializer.Meta.fields + ("request_status",)

    def get_request_status(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return ClassRequestService().get_user_request_status(user=user, class_obj=obj)
        return None


class ClassManagementSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    request_status = serializers.SerializerMethodField()

    class Meta:
        model = ClassManagement
        fields = (
            "course",
            "progress",
            "mark",
            "is_done_quiz",
            "status",
            "request_status",
        )

    def get_request_status(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return ClassRequestService().get_user_request_status(user=user, class_obj=obj.course)
        return None

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop("course")
        user = self.context.get("request").user

        for index, lesson in enumerate(course_representation["lessons"]):
            course_representation["lessons"][index]["docs_completed"] = CourseDocumentManagement.objects.filter(
                user=user,
                course_id=course_representation['id'],
                document_id__in=[doc_id["id"] for doc_id in lesson["documents"]],
                is_completed=True,
                is_available=True,
            ).values_list('document', flat=True)
            course_representation['lessons'][index]['videos_completed'] = VideoManagement.objects.filter(
                user=user,
                course_id=course_representation['id'],
                video_id__in=[video_id["id"] for video_id in lesson["videos"]],
                is_completed=True,
                is_available=True,
            ).values_list('video', flat=True)

        quiz_detail = {}
        quiz_answers = []
        correct_answers = 0
        total_answers = Answer.objects.filter(quiz__course_id=course_representation['id'], user=user)
        for answer in total_answers:
            quiz_answers.append({
                "quiz_id": answer.quiz_id,
                "answer_choice": answer.choice,
                "correct_answer": answer.quiz.correct_answer.choice
            })
            if answer.choice == answer.quiz.correct_answer.choice:
                correct_answers += 1

        quiz_detail['correct_answers'] = correct_answers
        quiz_detail['total_quiz'] = len(total_answers)
        quiz_detail['quiz_answers'] = quiz_answers
        course_representation['quiz_detail'] = quiz_detail

        for key in course_representation:
            representation[key] = course_representation[key]

        representation.pop("sold")
        representation.pop("price")

        return representation


class ListClassSerializer(serializers.ModelSerializer):
    request_status = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = (
            "id",
            "name",
            "request_status",
            "course_of_class",
            "thumbnail",
        )

    def get_request_status(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return ClassRequestService().get_user_request_status(user=user, class_obj=obj)
        return None



