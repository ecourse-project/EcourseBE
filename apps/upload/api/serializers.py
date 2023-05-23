from rest_framework import serializers
from apps.upload.models import UploadFile, UploadImage, UploadVideo
from django.conf import settings


class UploadVideoSerializer(serializers.ModelSerializer):
    video_path = serializers.SerializerMethodField()

    class Meta:
        model = UploadVideo
        fields = (
            "id",
            "video_name",
            "video_size",
            "video_path",
            "video_type",
            "duration",
            "video_embedded_url",
            "use_embedded_url",
        )

    @classmethod
    def get_video_path(cls, obj):
        if obj.video_path:
            return settings.BASE_URL + obj.video_path.url
        return ""

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        representation["file_name"] = representation.pop("video_name")
        representation["file_size"] = representation.pop("video_size")
        representation["file_path"] = representation.pop("video_path")
        representation["file_type"] = representation.pop("video_type")
        representation["file_embedded_url"] = representation.pop("video_embedded_url")

        return representation


class UploadFileSerializer(serializers.ModelSerializer):
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = UploadFile
        fields = (
            "id",
            "file_name",
            "file_size",
            "file_path",
            "file_type",
            "file_embedded_url",
            "use_embedded_url",
        )

    @classmethod
    def get_file_path(cls, obj):
        return settings.BASE_URL + obj.file_path.url


class UploadImageSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()

    class Meta:
        model = UploadImage
        fields = (
            "id",
            "image_size",
            "image_path",
            "image_type",
        )

    @classmethod
    def get_image_path(cls, obj):
        return settings.BASE_URL + obj.image_path.url
