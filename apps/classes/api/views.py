from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination
from apps.classes.api.serializers import ListClassSerializer, ClassManagementSerializer, ClassSerializer
from apps.classes.models import ClassRequest, Class
from apps.classes.services.services import ClassesService, ClassRequestService, ClassManagementService
from apps.classes.enums import ACCEPTED
from apps.courses.services.services import CourseManagementService
from apps.core.general.services import CustomListDataServices, CustomDictDataServices
from apps.core.general.enums import REQUEST_STATUS, CLASS_EXTRA_FIELDS
from apps.core.general.validate import check_class_course


class JoinRequestView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        class_id = self.request.data.get("class_id")
        class_obj = ClassesService().get_all_classes_queryset.filter(id=class_id).first()
        if ClassRequest.objects.filter(class_request=class_obj, user=self.request.user, accepted=False).exists():
            ClassRequest.objects.filter(class_request=class_obj, user=self.request.user, accepted=False).delete()
        else:
            ClassRequest.objects.create(class_request=class_obj, user=self.request.user)
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        custom_data = CustomListDataServices(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                custom_data.custom_response_list_data(
                    data=serializer.data,
                    fields=[REQUEST_STATUS],
                    user=request.user,
                    class_objs=queryset
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            custom_data.custom_response_list_data(
                data=serializer.data,
                fields=[REQUEST_STATUS],
                class_objs=queryset
            )
        )


class ClassDetailView(generics.RetrieveAPIView):
    serializer_class = ClassSerializer

    @staticmethod
    def is_accepted(user, class_obj):
        return ClassRequestService().get_user_request_status(user=user, class_obj=class_obj) == ACCEPTED

    def get_serializer_class(self):
        class_obj = ClassesService().get_all_classes_queryset.filter(id=self.request.query_params.get("class_id")).first()
        if self.is_accepted(self.request.user, class_obj):
            return ClassManagementSerializer
        return self.serializer_class

    def get_object(self):
        class_id = self.request.query_params.get("class_id")
        user = self.request.user
        class_obj = ClassesService().get_all_classes_queryset.filter(id=class_id).first()

        if self.is_accepted(self.request.user, class_obj):
            return ClassManagementService(user=user).get_class_management_queryset.filter(course=class_obj).first()
        return class_obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        class_obj = instance if check_class_course(instance) else instance.course
        custom_data = CustomDictDataServices(user=request.user)
        return Response(
            custom_data.custom_response_dict_data(
                data=serializer.data,
                fields=CLASS_EXTRA_FIELDS,
                class_objs=class_obj,
            )
        )


class HomepageClassListAPIView(generics.ListAPIView):
    serializer_class = ListClassSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    authentication_classes = ()

    def get_queryset(self):
        topic = self.request.query_params.get("topic")
        list_id = self.request.query_params.getlist("class_id")
        if topic:
            return ClassesService().get_classes_by_topic(topic)
        elif list_id:
            return ClassesService().get_classes_by_list_id(list_id)
        else:
            return ClassesService().get_all_classes_queryset



