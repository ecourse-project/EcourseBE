from rest_framework import serializers

from apps.users.choices import TEACHER
from apps.core.utils import get_summary_content, create_serializer_class
from apps.courses.models import Course, Lesson, CourseTopic, CourseDocument, CourseManagement
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer, UploadVideoSerializer


class CourseDocumentSerializer(serializers.ModelSerializer):
    file = UploadFileSerializer()

    class Meta:
        model = CourseDocument
        fields = (
            "id",
            "modified",
            "name",
            "description",
            "topic",
            "file",
        )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTopic
        fields = (
            "id",
            "name",
        )


class LessonSerializer(serializers.ModelSerializer):
    videos = UploadVideoSerializer(many=True)
    documents = CourseDocumentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "lesson_number",
            "content",
            "videos",
            "documents",
            "quiz_location",
        )


class CourseSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()
    lessons = LessonSerializer(many=True)
    topic = TopicSerializer()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "author",
            "modified",
            "name",
            "topic",
            "description",
            "course_of_class",
            "price",
            "sold",
            "lessons",
            "thumbnail",
            "test",
        )

    def get_author(self, obj):
        if obj.author and obj.author.role == TEACHER:
            return obj.author.full_name
        return ""

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        price = representation.get("price")
        if price is not None:
            representation["price"] = 0

        return representation


class CourseManagementSerializer(serializers.ModelSerializer):
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


class ListCourseSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()
    topic = TopicSerializer()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "author",
            "modified",
            "name",
            "topic",
            "description",
            "price",
            "sold",
            "thumbnail",
            "test",
        )

    def get_author(self, obj):
        if obj.author and obj.author.role == TEACHER:
            return obj.author.full_name
        return ""


class ListCourseManagementSerializer(serializers.ModelSerializer):
    course = ListCourseSerializer()
    # my_rating = serializers.SerializerMethodField()

    class Meta:
        model = CourseManagement
        fields = (
            # "my_rating",
            "course",
            "is_favorite",
            "status",
            "sale_status",
            "progress",
        )

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        for key in course_representation:
            representation[key] = course_representation[key]
        return representation

    # def get_my_rating(self, obj):
    #     course_rating = obj.course.rating_obj
    #     my_rating = course_rating.ratings.filter(user=self.context['request'].user).first()
    #     return RatingSerializer(my_rating).data if my_rating else {}


class AllCourseSerializer(serializers.ModelSerializer):
    lesson_serializer = create_serializer_class(Lesson, ["id", "name"])
    lessons = lesson_serializer(many=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "author",
            "name",
            "course_of_class",
            "lessons",
        )

    def get_author(self, obj):
        if obj.author and obj.author.role == TEACHER:
            return obj.author.full_name
        return ""

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        name = representation.pop("name", None)
        representation["name"] = (
            f"{'CLASS' if representation['course_of_class'] else 'COURSE'} - {get_summary_content(name)}"
        )
        return representation
