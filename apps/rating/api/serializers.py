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
        )


class DocumentRatingSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(many=True)

    class Meta:
        model = DocumentRating
        fields = "__all__"


class CourseRatingSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(many=True)

    class Meta:
        model = CourseRating
        fields = "__all__"
