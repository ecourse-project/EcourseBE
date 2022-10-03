from rest_framework import serializers

from apps.documents.api.serializers import DocumentSerializer
from apps.courses.api.serializers import CourseSerializer
from apps.carts.models import Cart, FavoriteList


class CartSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True)
    courses = CourseSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'total_price',
            'documents',
            'courses',
        )


class FavoriteListSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True)
    courses = CourseSerializer(many=True)

    class Meta:
        model = FavoriteList
        fields = (
            'id',
            'documents',
            'courses',
        )
