from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination
from apps.courses.models import CourseManagement, CourseDocument
from apps.courses.api.serializers import CourseManagementSerializer, ListCourseManagementSerializer
from apps.courses.services import CourseManagementService
from apps.courses.enums import BOUGHT
from apps.courses.exceptions import NoItemException
from apps.upload.models import UploadFile


class MostDownloadedCourseView(generics.ListAPIView):
    serializer_class = ListCourseManagementSerializer

    def get_queryset(self):
        service = CourseManagementService(self.request.user)
        service.init_courses_management()
        return service.get_course_mngt_queryset_by_selling.order_by('-course__sold')


class CourseListView(generics.ListAPIView):
    serializer_class = ListCourseManagementSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        service = CourseManagementService(self.request.user)
        service.init_courses_management()
        return service.get_course_mngt_queryset_by_selling.order_by('course__name')


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
        return Response(self.get_serializer(instance).data)


class UpdateCourseDocumentProgress(APIView):
    def get(self, request, *args, **kwargs):
        course_mngt = CourseManagement.objects.filter(
            course_id=self.request.query_params.get('course_id'), user=request.user, sale_status=BOUGHT).first()
        course_doc = CourseDocument.objects.filter(id=self.request.query_params.get('course_doc_id')).first()
        if not course_mngt:
            raise NoItemException
        if not course_doc:
            raise NoItemException("Document does not exist.")
        is_completed = CourseManagementService(request.user).add_doc_completed(course_mngt, course_doc)
        return Response({'is_completed': is_completed}, status=status.HTTP_200_OK)


class UpdateCourseVideoProgress(APIView):
    def get(self, request, *args, **kwargs):
        course_mngt = CourseManagement.objects.filter(
            course_id=self.request.query_params.get('course_id'), user=request.user, sale_status=BOUGHT).first()
        video = UploadFile.objects.filter(id=self.request.query_params.get('file_id')).first()
        if not course_mngt:
            raise NoItemException
        if not video:
            raise NoItemException("Video does not exist.")
        is_completed = CourseManagementService(request.user).add_video_completed(course_mngt, video)
        return Response({'is_completed': is_completed}, status=status.HTTP_200_OK)


# class UpdateLessonProgress(APIView):
#     def get(self, request, *args, **kwargs):
#         course_mngt = CourseManagement.objects.filter(
#             course_id=self.request.query_params.get('course_id'), user=request.user, sale_status=BOUGHT).first()
#         if not course_mngt:
#             raise NoItemException
#
#         videos_id = self.request.query_params.get('videos', [])
#         docs_id = self.request.query_params.get('documents', [])
