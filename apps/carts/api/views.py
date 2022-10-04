from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.carts.services import CartService, FavoriteListService
from apps.documents.models import Document
from apps.documents.api.serializers import DocumentManagementSerializer
from apps.courses.models import Course
from apps.courses.api.serializers import CourseManagementSerializer
from apps.carts.services import MoveItems


class CartInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cart_service = CartService(request.user.cart)
        cart_service.calculate_total_price()
        return Response(cart_service.custom_cart_data, status=status.HTTP_200_OK)


class FavoriteListInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        favorite_list_service = FavoriteListService(request.user.favorite_list)
        return Response(data=favorite_list_service.custom_favorite_list_data, status=status.HTTP_200_OK)


class MoveItemsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        move_items = MoveItems(self.request.user)
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        document = Document.objects.filter(id=self.request.query_params.get('item_id')).first()
        course = Course.objects.filter(id=self.request.query_params.get('item_id')).first()

        if document:
            doc_mngt = move_items.move_doc(start=start, end=end, doc=document)
            return Response(DocumentManagementSerializer(doc_mngt).data, status=status.HTTP_200_OK)
        elif course:
            course_mngt = move_items.move_course(start=start, end=end, course=course)
            return Response(CourseManagementSerializer(course_mngt).data, status=status.HTTP_200_OK)

        return Response({"message": "Cannot find document or course."}, status=status.HTTP_200_OK)
