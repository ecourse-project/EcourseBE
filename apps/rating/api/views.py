from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rating.models import Rating, DocumentRating, CourseRating
from apps.rating.api.serializers import RatingSerializer, DocumentRatingSerializer, CourseRatingSerializer
from apps.rating.exceptions import UserHasBeenRateException
from apps.documents.models import Document
from apps.courses.models import Course
from apps.courses.exceptions import NoItemException


class DocumentRateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        document_rating, _ = DocumentRating.objects.get_or_create(document_id=data.get("document_id"))
        if document_rating.rating.filter(user=request.user).first():
            raise UserHasBeenRateException
        rating = Rating.objects.create(user=request.user, rating=data.get('rating'), comment=data.get('comment'))
        document_rating.rating.add(rating)
        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)


class CourseRateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        course_rating, _ = CourseRating.objects.get_or_create(course_id=data.get("course_id"))
        if course_rating.rating.filter(user=request.user).first():
            raise UserHasBeenRateException("User has been rate this course")
        rating = Rating.objects.create(user=request.user, rating=data.get('rating'), comment=data.get('comment'))
        course_rating.rating.add(rating)
        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)


class DocumentListRate(generics.RetrieveAPIView):
    serializer_class = DocumentRatingSerializer

    def get_object(self):
        document_id = self.request.query_params.get('document_id')
        if not Document.objects.filter(id=document_id).first():
            raise NoItemException("Document does not exist.")
        return DocumentRating.objects.get(document_id=document_id)


class CourseListRate(generics.RetrieveAPIView):
    serializer_class = CourseRatingSerializer

    def get_object(self):
        course_id = self.request.query_params.get('course_id')
        if not Course.objects.filter(id=course_id).first():
            raise NoItemException
        return CourseRating.objects.get(course_id=course_id)

