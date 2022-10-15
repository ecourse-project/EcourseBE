from rest_framework import serializers

from apps.users.api.serializers import UserSerializer
from apps.rating.models import Rating, DocumentRating, CourseRating


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rating
        fields = (
            "id",
            "created",
            "modified",
            "user",
            "rating",
            "comment",
        )


class DocumentRatingSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(many=True)

    class Meta:
        model = DocumentRating
        fields = (
            "id",
            "document",
            "rating",
        )


class CourseRatingSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(many=True)

    class Meta:
        model = CourseRating
        fields = (
            "id",
            "course",
            "rating",
        )
