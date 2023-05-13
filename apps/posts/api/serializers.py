from rest_framework import serializers

from apps.posts.models import Post
from apps.upload.api.serializers import UploadImageSerializer


class ListPostSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "thumbnail",
        )


class PostSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(max_length=50, trim_whitespace=True)
    thumbnail = UploadImageSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "created",
            "modified",
            "name",
            "topic",
            "content",
            "thumbnail",
        )

