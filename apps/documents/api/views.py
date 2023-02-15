from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.documents.api.serializers import DocumentSerializer, DocumentManagementSerializer
from apps.documents.services.services import DocumentManagementService, DocumentService
from apps.documents.enums import BOUGHT
from apps.documents.models import DocumentManagement
from apps.core.pagination import StandardResultsSetPagination


class MostDownloadedDocumentView(generics.ListAPIView):
    serializer_class = DocumentManagementSerializer

    def get_queryset(self):
        service = DocumentManagementService(self.request.user)
        return service.get_doc_mngt_queryset_by_selling.order_by('-document__sold')


class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentManagementSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        service = DocumentManagementService(self.request.user)
        title = self.request.query_params.get("title")
        list_id = self.request.query_params.getlist('document_id')
        if title:
            return service.get_doc_mngt_queryset_by_selling.filter(document__title__name__icontains=title)
        elif list_id:
            return service.get_documents_mngt_by_list_id(list_id)
        else:
            return service.get_doc_management_queryset


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


# ==========================> NEW REQUIREMENTS

class HomepageDocumentListAPIView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        title = self.request.query_params.get("title")
        list_id = self.request.query_params.getlist('document_id')
        if title:
            return DocumentService().get_documents_by_title(title)
        elif list_id:
            return DocumentService().get_documents_by_list_id(list_id)
        else:
            return DocumentService().get_all_documents_queryset









