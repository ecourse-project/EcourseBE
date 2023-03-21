from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination
from apps.classes.api.serializers import ListClassSerializer, ClassSerializer
from apps.classes.models import ClassRequest
from apps.classes.services.services import ClassesService


class JoinRequestView(APIView):
    def post(self, request, *args, **kwargs):
        ClassRequest.objects.get_or_create(class_request_id=self.request.data.get("class_id"), user=self.request.user)
        return Response(status=status.HTTP_200_OK)


class ClassListView(generics.ListAPIView):
    serializer_class = ListClassSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.request.query_params.get("topic"):
            return ClassesService().get_classes_by_topic(self.request.query_params.get("topic"))
        return ClassesService().get_all_classes_queryset


class ClassDetailView(generics.RetrieveAPIView):
    serializer_class = ClassSerializer

    def get_object(self):
        return ClassesService().get_all_classes_queryset.filter(id=self.request.query_params.get("class_id")).first()



