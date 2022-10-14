from rest_framework import serializers
from apps.courses.models import Course, Lesson, Topic, CourseDocument, CourseManagement
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer


class CourseDocumentSerializer(serializers.ModelSerializer):
    file = UploadFileSerializer()

    class Meta:
        model = CourseDocument
        fields = (
            "id",
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
            "name",
        )


class LessonSerializer(serializers.ModelSerializer):
    videos = UploadFileSerializer(many=True)
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
        )


class CourseSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()
    lessons = LessonSerializer(many=True)
    topic = TopicSerializer()

    class Meta:
        model = Course
        fields = (
            "id",
            "modified",
            "name",
            "topic",
            "description",
            "price",
            "sold",
            "lessons",
            "thumbnail",
            "views",
            "rating",
            "num_of_rates",
        )


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
            "docs_completed",
            "videos_completed",
        )

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')

        for key in course_representation:
            representation[key] = course_representation[key]
            if key == 'lessons':
                for count, lesson in enumerate(representation[key], start=0):
                    lesson_obj = Lesson.objects.filter(id=representation[key][count]['id']).first()
                    lesson_video_complete = lesson_obj.videos.all().filter(id__in=representation["videos_completed"]).count()
                    lesson_doc_complete = lesson_obj.documents.all().filter(id__in=representation["docs_completed"]).count()
                    if (lesson_obj.total_documents + lesson_obj.total_videos) != 0:
                        representation[key][count]['progress'] = round(
                            (lesson_video_complete + lesson_doc_complete) * 100 /
                            (lesson_obj.total_documents + lesson_obj.total_videos)
                        )
                    else:
                        representation[key][count]['progress'] = 0
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

    class Meta:
        model = Course
        fields = (
            "id",
            "modified",
            "name",
            "topic",
            "description",
            "price",
            "sold",
            "thumbnail",
            "views",
            "rating",
            "num_of_rates",
        )


class ListCourseManagementSerializer(serializers.ModelSerializer):
    course = ListCourseSerializer()

    class Meta:
        model = CourseManagement
        fields = (
            "course",
            "is_favorite",
            "status",
            "sale_status"
        )

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        course_representation = representation.pop('course')
        for key in course_representation:
            representation[key] = course_representation[key]
        return representation

