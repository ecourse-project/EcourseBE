from rest_framework import serializers

from apps.courses.api.serializers import LessonSerializer, TopicSerializer, CourseSerializer, CourseManagementSerializer
from apps.classes.models import Class, ClassManagement
from apps.classes.services.services import ClassRequestService
from apps.classes.enums import ACCEPTED
from apps.upload.api.serializers import UploadImageSerializer
from apps.users.choices import MANAGER


class ClassSerializer(CourseSerializer):
    request_status = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)
    topic = TopicSerializer()

    class Meta:
        model = Class
        fields = CourseSerializer.Meta.fields + ("request_status",)

    def get_request_status(self, obj):
        user = self.context.get("request").user if self.context.get("request") else None
        if user and user.is_authenticated:
            class_mngt = ClassManagement.objects.filter(user=user, course=obj).first()
            return (
                ACCEPTED
                if class_mngt and class_mngt.user_in_class
                else ClassRequestService().get_user_request_status(user=user, class_obj=obj)
            )
        return None

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation.pop("sold", None)
        representation.pop("price", None)
        return representation


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
            return (
                ACCEPTED
                if obj.user_in_class
                else ClassRequestService().get_user_request_status(user=user, class_obj=obj.course)
            )
        return None

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop("course")

        for key in course_representation:
            representation[key] = course_representation[key]

        representation.pop("sold", None)
        representation.pop("price", None)

        return representation


class ListClassSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()

    class Meta:
        model = Class
        fields = (
            "id",
            "name",
            "course_of_class",
            "thumbnail",
            "test",
        )
