from rest_framework import serializers
from apps.courses.models import Course, Lesson, Topic, CourseDocument, CourseManagement
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer
from apps.upload.models import UploadFile


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


class CourseManagementSerializer(serializers.ModelSerializer):
    course = CourseSerializer()


    class Meta:
        model = CourseManagement
        fields = (
            "course",
            # "progress",
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
        docs_completed = representation["docs_completed"]
        videos_completed = representation["videos_completed"]
        total = 0
        total_complete = 0

        for key in course_representation:
            representation[key] = course_representation[key]
            if key == 'lessons':
                for count, lesson in enumerate(representation[key], start=0):
                    lesson_obj = Lesson.objects.filter(id=representation[key][count]['id']).first()
                    lesson_videos = lesson_obj.videos.all()
                    lesson_docs = lesson_obj.documents.all()
                    total += lesson_videos.count() + lesson_docs.count()
                    lesson_video_complete = lesson_videos.filter(id__in=videos_completed).count()
                    lesson_doc_complete = lesson_docs.filter(id__in=docs_completed).count()
                    total_complete += lesson_video_complete + lesson_doc_complete
                    representation[key][count]['progress'] = int(
                        (lesson_video_complete + lesson_doc_complete) * 100 / (lesson_videos.count() + lesson_docs.count()))
        if total != 0:
            representation["progress"] = int(total_complete * 100 / total)
            # obj.save(update_fields=['progress'])
        else:
            representation["progress"] = 0
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

