from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination
from apps.courses.models import CourseManagement
from apps.courses.api.serializers import (
    CourseManagementSerializer,
    ListCourseManagementSerializer,
    ListCourseSerializer,
)
from apps.courses.services.services import CourseManagementService, CourseService
from apps.courses.enums import BOUGHT


class MostDownloadedCourseView(generics.ListAPIView):
    serializer_class = ListCourseManagementSerializer

    def get_queryset(self):
        return CourseManagementService(self.request.user).get_course_mngt_queryset_by_selling.order_by('-course__sold')


class CourseListView(generics.ListAPIView):
    serializer_class = ListCourseManagementSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)

    def get_queryset(self):
        service = CourseManagementService(self.request.user)
        title = self.request.query_params.get("title")
        list_id = self.request.query_params.getlist('course_id')
        if title:
            return service.get_course_mngt_queryset_by_selling.filter(course__title__name__icontains=title)
        elif list_id:
            return service.get_courses_mngt_by_list_id(list_id)
        else:
            return service.get_course_management_queryset


class UserCoursesListView(generics.ListAPIView):
    serializer_class = ListCourseManagementSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        service = CourseManagementService(self.request.user)
        return service.get_course_management_queryset.filter(sale_status=BOUGHT).order_by('course__name')


class CourseRetrieveView(generics.RetrieveAPIView):
    serializer_class = CourseManagementSerializer

    def get_object(self):
        course_id = self.request.query_params.get('course_id')
        return CourseManagement.objects.get(user=self.request.user, course_id=course_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sale_status != BOUGHT:
            course = instance.course
            course.views += 1
            course.save(update_fields=['views'])
        service = CourseManagementService(request.user)
        return Response(
            service.custom_course_detail_data(self.get_serializer(instance).data)
        )


class UpdateLessonProgress(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        CourseManagementService(request.user).update_lesson_progress(
            course_id=data.get('course_id'),
            lessons=data.get('lessons'),
        )
        return Response(status=status.HTTP_200_OK)


# ==========================> NEW REQUIREMENTS

class HomepageCourseListAPIView(generics.ListAPIView):
    serializer_class = ListCourseSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        title = self.request.query_params.get("title")
        list_id = self.request.query_params.getlist('course_id')
        if title:
            return CourseService().get_courses_by_title(title)
        elif list_id:
            return CourseService().get_courses_by_list_id(list_id)
        else:
            return CourseService().get_all_courses_queryset
