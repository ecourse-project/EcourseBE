from rest_framework import serializers
from apps.upload.models import UploadFile, UploadImage


class UploadFileSerializer(serializers.ModelSerializer):
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = UploadFile
        fields = (
            "id",
            "file_name",
            "file_path",
            "file_size",
            "file_type",
            "duration",
        )

    @classmethod
    def get_file_path(cls, obj):
        return "http://127.0.0.1:4000" + obj.file_path.url


class UploadImageSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()

    class Meta:
        model = UploadImage
        fields = (
            "id",
            "image_path",
            "image_size",
            "image_type",
        )

    @classmethod
    def get_image_path(cls, obj):
        return "http://127.0.0.1:4000" + obj.image_path.url
