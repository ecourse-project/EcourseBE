from rest_framework import serializers

from apps.posts.models import Post
from apps.upload.api.serializers import UploadImageSerializer


class PostSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(max_length=50, trim_whitespace=True)
    thumbnail = UploadImageSerializer()
    images = UploadImageSerializer(many=True)

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
            "images",
        )

