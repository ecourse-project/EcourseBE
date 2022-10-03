from rest_framework import serializers

from apps.documents.models import Document, DocumentManagement
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer


class DocumentSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()
    file = UploadFileSerializer()
    name = serializers.CharField(max_length=100, trim_whitespace=True)
    title = serializers.CharField(max_length=50, trim_whitespace=True)
    description = serializers.CharField(trim_whitespace=True)

    class Meta:
        model = Document
        fields = (
            'id',
            "created",
            "modified",
            'name',
            'description',
            'title',
            'price',
            'sold',
            'thumbnail',
            'file',
            'is_selling',
            'views',
            'rating',
            'num_of_rates',
        )


class DocumentManagementSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        model = DocumentManagement
        fields = (
            "document",
            "sale_status",
            "is_favorite",
        )

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        document_representation = representation.pop('document')
        for key in document_representation:
            representation[key] = document_representation[key]

        return representation
