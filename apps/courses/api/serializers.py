from rest_framework import serializers
from apps.courses.models import Course, Lesson, Topic, CourseDocument, CourseManagement
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer


class CourseDocumentSerializer(serializers.ModelSerializer):
    file = UploadFileSerializer()

    class Meta:
        model = CourseDocument
        fields = (
            "id",
            "created",
            "modified",
            "name",
            "description",
            "title",
            "file",
        )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            "id",
            "created",
            "modified",
            "name",
        )


class LessonSerializer(serializers.ModelSerializer):
    videos = UploadFileSerializer(many=True)
    documents = CourseDocumentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "created",
            "modified",
            "name",
            "lesson_number",
            "content",
            "videos",
            "documents",
        )


class CourseSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()
    lessons = LessonSerializer(many=True)
    topic = TopicSerializer()

    class Meta:
        model = Course
        fields = (
            "id",
            "created",
            "modified",
            "name",
            "topic",
            "description",
            "price",
            "sold",
            "lessons",
            "thumbnail",
            "is_selling",
            "views",
            "rating",
            "num_of_rates",
        )


class CourseManagementSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CourseManagement
        fields = (
            "course",
            "progress",
            "status",
            "sale_status",
            "mark",
            "is_done_quiz",
            "is_favorite",
        )

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        for key in course_representation:
            representation[key] = course_representation[key]

        return representation

    # def to_internal_value(self, data):
    #     """Move fields related to profile to their own profile dictionary."""
    #     profile_internal = {}
    #     for key in ProfileSerializer.Meta.fields:
    #         if key in data:
    #             profile_internal[key] = data.pop(key)
    #
    #     internal = super().to_internal_value(data)
    #     internal['profile'] = profile_internal
    #     return internal
    #
    # def update(self, instance, validated_data):
    #     """Update user and profile. Assumes there is a profile for every user."""
    #     profile_data = validated_data.pop('profile')
    #     super().update(instance, validated_data)
    #
    #     profile = instance.profile
    #     for attr, value in profile_data.items():
    #         setattr(profile, attr, value)
    #     profile.save()
    #
    #     return instance

