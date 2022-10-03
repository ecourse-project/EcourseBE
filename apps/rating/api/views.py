from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rating.models import Rating, DocumentRating, CourseRating
from apps.rating.api.serializers import RatingSerializer, DocumentRatingSerializer, CourseRatingSerializer


class DocumentRateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        document_rating, _ = DocumentRating.objects.get_or_create(document_id=data.get("document_id"))
        rating = Rating.objects.create(user=request.user, rating=data.get('rating'))
        document_rating.rating.add(rating)
        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)


class CourseRateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        course_rating, _ = CourseRating.objects.get_or_create(course_id=data.get("course_id"))
        rating = Rating.objects.create(user=request.user, rating=data.get('rating'))
        course_rating.rating.add(rating)
        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
