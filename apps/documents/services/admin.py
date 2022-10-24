from apps.documents.models import DocumentManagement
from django.utils.timezone import localtime


class DocumentAdminService:
    def __init__(self, user):
        self.user = user

    def update_document_sale_status(self, documents, sale_status):
        DocumentManagement.objects.filter(
            user=self.user, document__in=documents
        ).update(sale_status=sale_status, last_update=localtime())


def init_doc_mngt(document, users):
    DocumentManagement.objects.bulk_create([DocumentManagement(document=document, user=user) for user in users])
