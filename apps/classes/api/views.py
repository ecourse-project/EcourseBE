from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination
from apps.classes.api.serializers import ListClassSerializer, ClassSerializer
from apps.classes.models import ClassRequest
from apps.classes.services.services import ClassesService, ClassRequestService


class JoinRequestView(APIView):
    def post(self, request, *args, **kwargs):
        class_id = self.request.data.get("class_id")
        ClassRequest.objects.get_or_create(class_request_id=class_id, user=self.request.user)
        class_obj = ClassesService().get_all_classes_queryset.filter(id=class_id).first()
        user = self.request.user
        return Response(
            data={"request_status": ClassRequestService().get_user_request_status(user, class_obj)},
            status=status.HTTP_200_OK
        )


class ClassListView(generics.ListAPIView):
    serializer_class = ListClassSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        service = ClassesService()
        topic = self.request.query_params.get("topic")
        list_id = self.request.query_params.getlist('class_id')
        if topic:
            return service.get_classes_by_topic(topic)
        elif list_id:
            return service.get_classes_by_list_id(list_id)
        else:
            return service.get_all_classes_queryset


class ClassDetailView(generics.RetrieveAPIView):
    serializer_class = ClassSerializer

    def get_object(self):
        return ClassesService().get_all_classes_queryset.filter(id=self.request.query_params.get("class_id")).first()


class HomepageClassListAPIView(generics.ListAPIView):
    serializer_class = ListClassSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    authentication_classes = ()

    def get_queryset(self):
        topic = self.request.query_params.get("topic")
        list_id = self.request.query_params.getlist('course_id')
        if topic:
            return ClassesService().get_classes_by_topic(topic)
        elif list_id:
            return ClassesService().get_classes_by_list_id(list_id)
        else:
            return ClassesService().get_all_classes_queryset



