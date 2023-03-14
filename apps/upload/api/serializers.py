from rest_framework import serializers
from apps.upload.models import UploadFile, UploadImage
from django.conf import settings


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
            "duration",
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
