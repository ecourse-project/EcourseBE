from rest_framework import generics
from rest_framework.response import Response

from apps.core.pagination import StandardResultsSetPagination
from apps.courses.models import CourseManagement
from apps.courses.api.serializers import CourseManagementSerializer
from apps.courses.services import CourseManagementService
from apps.courses.enums import BOUGHT


class MostDownloadedCourseView(generics.ListAPIView):
    serializer_class = CourseManagementSerializer

    def get_queryset(self):
        service = CourseManagementService(self.request.user)
        service.init_courses_management()
        return service.get_course_mngt_queryset_by_selling.order_by('-course__sold')


class CourseListView(generics.ListAPIView):
    serializer_class = CourseManagementSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        service = CourseManagementService(self.request.user)
        service.init_courses_management()
        return service.get_course_mngt_queryset_by_selling.order_by('course__name')


class UserCoursesListView(generics.ListAPIView):
    serializer_class = CourseManagementSerializer
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
        return Response(self.get_serializer(instance).data)
