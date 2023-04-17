from rest_framework import serializers

from apps.courses.api.serializers import LessonSerializer, TopicSerializer, CourseSerializer, CourseManagementSerializer
from apps.classes.models import Class, ClassManagement
from apps.classes.services.services import ClassRequestService


class ClassSerializer(CourseSerializer):
    request_status = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)
    topic = TopicSerializer()

    class Meta(CourseSerializer.Meta):
        model = Class
        fields = CourseManagementSerializer.Meta.fields + ("request_status",)

    def get_request_status(self, obj):
        user = self.context.get("request").user if self.context.get("request") else None
        if user and user.is_authenticated:
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
        user = self.context.get("request").user if self.context.get("request") else None
        if user and user.is_authenticated:
            return ClassRequestService().get_user_request_status(user=user, class_obj=obj.course)
        return None

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop("course")

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
        user = self.context.get("request").user if self.context.get("request") else None
        if user and user.is_authenticated:
            return ClassRequestService().get_user_request_status(user=user, class_obj=obj)
        return None



