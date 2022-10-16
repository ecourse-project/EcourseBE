from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination
from apps.courses.models import CourseManagement, CourseDocument
from apps.courses.api.serializers import CourseManagementSerializer, ListCourseManagementSerializer
from apps.courses.services import CourseManagementService, LessonManagementService
from apps.courses.enums import BOUGHT


class MostDownloadedCourseView(generics.ListAPIView):
    serializer_class = ListCourseManagementSerializer

    def get_queryset(self):
        course_mngt_service = CourseManagementService(self.request.user)
        course_mngt_service.init_courses_management()
        LessonManagementService(self.request.user).init_lessons_management()
        return course_mngt_service.get_course_mngt_queryset_by_selling.order_by('-course__sold')


class CourseListView(generics.ListAPIView):
    serializer_class = ListCourseManagementSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        course_mngt_service = CourseManagementService(self.request.user)
        course_mngt_service.init_courses_management()
        LessonManagementService(self.request.user).init_lessons_management()
        return course_mngt_service.get_course_mngt_queryset_by_selling.order_by('course__name')


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
        CourseManagementService(request.user).update_lesson_progress(lessons=self.request.data)
        return Response(status=status.HTTP_200_OK)


