from datetime import datetime, timedelta

from rest_framework import serializers

from apps.documents.models import Document, DocumentManagement
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer
from apps.documents.enums import BOUGHT
from apps.payment.enums import SUCCESS
from apps.payment.models import Order
from apps.configuration.models import Configuration


class DocumentSerializer(serializers.ModelSerializer):
    thumbnail = UploadImageSerializer()
    file = UploadFileSerializer()
    name = serializers.CharField(max_length=100, trim_whitespace=True)
    topic = serializers.CharField(max_length=50, trim_whitespace=True)
    description = serializers.CharField(trim_whitespace=True)

    class Meta:
        model = Document
        fields = (
            'id',
            "created",
            "modified",
            'name',
            'description',
            'topic',
            'price',
            'sold',
            'thumbnail',
            'file',
            'is_selling',
            'views',
            # 'rating',
            'num_of_rates',
        )


class DocumentManagementSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()
    download = serializers.SerializerMethodField()

    class Meta:
        model = DocumentManagement
        fields = (
            "document",
            "sale_status",
            "is_favorite",
            "download",
        )

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        document_representation = representation.pop('document')
        for key in document_representation:
            representation[key] = document_representation[key]

        return representation

    def get_download(self, obj):
        config = Configuration.objects.first()
        if config:
            if not config.document_unlimited_time:
                if obj.sale_status == BOUGHT and Configuration.objects.first():
                    user_order = Order.objects.filter(user=obj.user, status=SUCCESS, documents=obj.document).first()
                    document_time_limit = config.document_time_limit
                    if user_order and document_time_limit:
                        if (user_order.created + timedelta(hours=document_time_limit)).timestamp() > datetime.now().timestamp():
                            return True
                return False
        return True
