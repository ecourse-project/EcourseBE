from rest_framework import serializers

from apps.payment.models import Order
from apps.documents.api.serializers import DocumentManagementSerializer
from apps.documents.models import DocumentManagement
from apps.courses.api.serializers import CourseManagementSerializer
from apps.courses.models import CourseManagement


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
        doc_mngt = DocumentManagement.objects.filter(
            user=self.context['request'].user,
            document__in=obj.documents.all()
        )
        return DocumentManagementSerializer(doc_mngt, many=True).data

    def get_courses(self, obj):
        course_mngt = CourseManagement.objects.filter(
            user=self.context['request'].user,
            course__in=obj.courses.all()
        )
        return CourseManagementSerializer(course_mngt, many=True).data

