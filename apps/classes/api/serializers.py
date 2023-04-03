from rest_framework import serializers

from apps.courses.api.serializers import LessonSerializer, TopicSerializer, CourseSerializer
from apps.classes.models import Class
from apps.classes.services.services import ClassRequestService


class ClassSerializer(CourseSerializer):
    request_status = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)
    topic = TopicSerializer()

    class Meta(CourseSerializer.Meta):
        model = Class
        fields = CourseSerializer.Meta.fields + ("request_status",)

    def get_request_status(self, obj):
        return ClassRequestService().get_user_request_status(
            user=self.context.get("request").user, class_obj=obj,
        )


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
        return ClassRequestService().get_user_request_status(
            user=self.context.get("request").user, class_obj=obj,
        )


