from rest_framework import serializers

from apps.courses.api.serializers import CourseSerializer
from apps.classes.models import Class, ClassRequest
from apps.classes.services.services import ClassRequestService


class ClassSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    request_status = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = (
            "id",
            "name",
            "course",
            "request_status",
        )

    def get_user_accepted(self, obj):
        return ClassRequestService().get_user_request_status(
            user=self.context.get("request").user, class_obj=obj,
        )


    def to_representation(self, obj):
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        course_representation.pop("price")
        course_representation.pop("sold")
        representation["course"] = course_representation
        return representation


class ListClassSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Class
        fields = (
            "id",
            "name",
            "course",
        )

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        course_representation.pop("price")
        course_representation.pop("sold")
        course_representation.pop("lessons")
        representation["course"] = course_representation
        return representation


