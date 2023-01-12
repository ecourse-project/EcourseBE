from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.documents.api.serializers import DocumentSerializer, DocumentManagementSerializer
from apps.documents.services.services import DocumentManagementService, DocumentService
from apps.documents.enums import BOUGHT
from apps.documents.models import DocumentManagement
from apps.upload.services.upload import upload_files, upload_images
from apps.core.pagination import StandardResultsSetPagination


class MostDownloadedDocumentView(generics.ListAPIView):
    serializer_class = DocumentManagementSerializer

    def get_queryset(self):
        service = DocumentManagementService(self.request.user)
        service.init_documents_management()
        return service.get_doc_mngt_queryset_by_selling.order_by('-document__sold')


class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentManagementSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        service = DocumentManagementService(self.request.user)
        service.init_documents_management()
        title = self.request.query_params.get("title")
        if title:
            return service.get_doc_mngt_queryset_by_selling.filter(document__title__name__icontains=title)
        return service.get_doc_mngt_queryset_by_selling


class HomepageDocumentListAPIView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        title = self.request.query_params.get("title")
        if title:
            return DocumentService().get_all_documents_queryset.filter(
                title__name__icontains=title,
                is_selling=True,
            )
        return DocumentService().get_all_documents_queryset.filter(is_selling=True)


class UserDocumentsListView(generics.ListAPIView):
    serializer_class = DocumentManagementSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        service = DocumentManagementService(self.request.user)
        return service.get_doc_management_queryset.filter(sale_status=BOUGHT)


class DocumentRetrieveView(generics.RetrieveAPIView):
    serializer_class = DocumentManagementSerializer

    def get_object(self):
        document_id = self.request.query_params.get('document_id')
        return DocumentManagement.objects.get(user=self.request.user, document_id=document_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sale_status != BOUGHT:
            doc = instance.document
            doc.views += 1
            doc.save(update_fields=['views'])
        service = DocumentManagementService(request.user)
        return Response(
            service.custom_doc_detail_data(self.get_serializer(instance).data)
        )

    # Not used
    # def perform_update(self, serializer):
    #     instance = serializer.instance
    #     instance.thumbnail.delete_image()
    #     instance.file.delete_file()
    #     data = self.request.data
    #     image_update = update_image(instance.thumbnail.id, data.getlist('image')[0], data.get('folder_name'))
    #     file_update = update_file(instance.file.id, data.getlist('file')[0], data.get('folder_name'))
    #     serializer.save(thumbnail=image_update, file=file_update)
    #
    # def perform_destroy(self, instance):
    #     instance.thumbnail.delete()
    #     instance.file.delete()
    #     instance.delete()





# Not used
# class DocumentCreateView(generics.CreateAPIView):
#     serializer_class = DocumentSerializer
#
#     def perform_create(self, serializer):
#         data = self.request.data
#         upload_thumbnail = upload_images(self.request, data.getlist('image'), data.get('folder_name'))
#         upload_file = upload_files(self.request, data.getlist('file'), data.get('folder_name'))
#         serializer.save(thumbnail=upload_thumbnail[0], file=upload_file[0])






