from datetime import datetime, timedelta

from rest_framework import serializers

from apps.documents.models import Document, DocumentManagement
from apps.documents.enums import BOUGHT
from apps.payment.enums import SUCCESS
from apps.payment.models import Order
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer
from apps.configuration.models import Configuration
from apps.users.choices import MANAGER


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
            'thumbnail',
            'file',
            'is_selling',
        )

    def to_representation(self, obj):
        representation = super().to_representation(obj)

        request = self.context.get("request")
        user = request.user if request else None
        if not user:
            return representation
        if user.is_anonymous or not user.is_authenticated:
            representation.pop("file", None)

        price = representation.get("price")
        if price is not None:
            representation["price"] = 0

        return representation


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
        representation = super().to_representation(obj)
        document_representation = representation.pop('document')
        for key in document_representation:
            representation[key] = document_representation[key]

        if representation.get("download") is False or not representation.get("sale_status") == BOUGHT:
            representation.pop("file", None)

        return representation

    def get_download(self, obj):
        request = self.context.get("request")
        config = Configuration.objects.first()
        is_unlimited = config.unlimited_document_time if config else True
        if request and not request.user.is_anonymous and request.user.role == MANAGER:
            return True
        if not is_unlimited:
            if obj.sale_status == BOUGHT and Configuration.objects.first():
                user_order = Order.objects.filter(user=obj.user, status=SUCCESS, documents=obj.document).first()
                document_time_limit = config.document_time_limit
                if user_order and document_time_limit:
                    if (user_order.created + timedelta(hours=document_time_limit)).timestamp() > datetime.now().timestamp():
                        return True
            return False
        else:
            if obj.sale_status == BOUGHT:
                user_order = Order.objects.filter(user=obj.user, status=SUCCESS, documents=obj.document).first()
                return True if user_order else False
            return False

