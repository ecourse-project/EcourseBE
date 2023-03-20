from rest_framework import serializers

from apps.courses.api.serializers import CourseSerializer
from apps.classes.models import Class


class ClassSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    user_accepted = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = (
            "id",
            "name",
            "course",
            "user_accepted",
        )

    def get_user_accepted(self, obj):
        if obj.users.filter(id=self.context.get("request").user.id).exists():
            return True
        return False

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
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
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        course_representation.pop("price")
        course_representation.pop("sold")
        course_representation.pop("lessons")
        representation["course"] = course_representation
        return representation


