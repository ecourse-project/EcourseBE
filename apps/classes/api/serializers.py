from rest_framework import serializers

from apps.courses.api.serializers import CourseSerializer, CourseManagementSerializer
from apps.classes.models import Class, ClassRequest
from apps.classes.services.services import ClassRequestService
from apps.courses.models import CourseManagement


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

    def get_request_status(self, obj):
        return ClassRequestService().get_user_request_status(
            user=self.context.get("request").user, class_obj=obj,
        )

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        course_id = course_representation["id"]
        user = self.context.get("request").user
        course_mngt = CourseManagementSerializer(CourseManagement.objects.filter(course_id=course_id, user=user).first()).data
        course_mngt.pop("price")
        course_mngt.pop("sold")
        representation["course"] = course_mngt
        return representation


class ListClassSerializer(serializers.ModelSerializer):
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

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        course_representation.pop("price")
        course_representation.pop("sold")
        course_representation.pop("lessons")
        representation["course"] = course_representation
        return representation

    def get_request_status(self, obj):
        return ClassRequestService().get_user_request_status(
            user=self.context.get("request").user, class_obj=obj,
        )


