from rest_framework import serializers

from apps.payment.models import Order
from apps.documents.api.serializers import DocumentManagementSerializer
from apps.documents.models import DocumentManagement, Document
from apps.courses.api.serializers import CourseManagementSerializer
from apps.courses.models import CourseManagement, Course
from apps.core.utils import create_serializer_class


class OrderSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'created',
            'code',
            'total_price',
            'status',
            'documents',
            'courses',
        )

    def get_documents(self, obj):
        documents = obj.documents.all()
        serializer_class = create_serializer_class(Document, ["id", "name", "description", "price"])
        return serializer_class(documents, many=True).data

    def get_courses(self, obj):
        courses = obj.courses.all()
        serializer_class = create_serializer_class(Course, ["id", "name", "description", "price"])
        return serializer_class(courses, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        total_price = representation.get("total_price")
        if total_price is not None:
            representation["total_price"] = 0

        return representation

