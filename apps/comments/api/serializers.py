from rest_framework import serializers

from apps.users.api.serializers import UserSerializer
from apps.comments.models import Comment, ReplyComment


class ReplyCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ReplyComment
        fields = (
            "id",
            "user",
            "created",
            "content",
        )


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    reply_comments = ReplyCommentSerializer(many=True)
    course_id = serializers.UUIDField(source="course.id")

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "created",
            "content",
            "course_id",
            "reply_comments",
        )