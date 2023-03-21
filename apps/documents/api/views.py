from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.documents.api.serializers import DocumentSerializer, DocumentManagementSerializer
from apps.documents.services.services import DocumentManagementService, DocumentService
from apps.documents.enums import BOUGHT
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
        topic = self.request.query_params.get("topic")
        list_id = self.request.query_params.getlist('document_id')
        if topic:
            return service.get_doc_mngt_queryset_by_selling.filter(document__topic__name__icontains=topic)
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
        return DocumentManagementService(
            user=self.request.user
        ).get_doc_management_queryset.filter(
            document_id=self.request.query_params.get('document_id')
        ).first()

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
    authentication_classes = ()

    def get_queryset(self):
        topic = self.request.query_params.get("topic")
        list_id = self.request.query_params.getlist('document_id')
        if topic:
            return DocumentService().get_documents_by_topic(topic)
        elif list_id:
            return DocumentService().get_documents_by_list_id(list_id)
        else:
            return DocumentService().get_all_documents_queryset









