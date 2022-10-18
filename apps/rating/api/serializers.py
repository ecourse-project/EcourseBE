from rest_framework import serializers

from apps.users.api.serializers import UserSerializer
from apps.rating.models import Rating, DocumentRating, CourseRating
from apps.users.models import User


class UserRatingInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "full_name",
            "avatar",
        )

    @classmethod
    def get_avatar(cls, obj):
        return obj.get_avatar()


class RatingSerializer(serializers.ModelSerializer):
    user = UserRatingInfoSerializer()

    class Meta:
        model = Rating
        fields = (
            "id",
            "created",
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
