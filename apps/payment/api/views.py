from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.payment.services import OrderService, generate_code
from apps.payment.models import Order
from apps.payment.api.serializers import OrderSerializer
from apps.payment.exceptions import NoItemsException
from apps.documents.models import Document
from apps.courses.models import Course
from apps.core.pagination import StandardResultsSetPagination


class CreateOrderView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = user.cart
        documents = Document.objects.filter(id__in=self.request.data.get('documents', []))
        courses = Course.objects.filter(id__in=self.request.data.get('courses', []))
        total_price = self.request.data.get('total_price', 0)
        if (not documents) and (not courses):
            raise NoItemsException

        order = Order.objects.create(user=user, code=generate_code(user))
        if documents:
            cart.documents.remove(*documents)
            OrderService(order).add_documents(documents=documents, user=user)
        if courses:
            cart.courses.remove(*courses)
            OrderService(order).add_courses(courses=courses, user=user)
        order.total_price = total_price
        order.save(update_fields=['total_price'])

        return Response(OrderService(order).custom_order_data(user=user), status=status.HTTP_201_CREATED)


class OrderRetrieveView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        order_id = self.request.query_params.get('order_id')
        return Order.objects.get(id=order_id)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')


class CancelOrderView(APIView):
    def get(self, request, *args, **kwargs):
        order_id = self.request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)
        OrderService(order).cancel_order()
        return Response({'message': 'Cancel order success.'}, status=status.HTTP_200_OK)











