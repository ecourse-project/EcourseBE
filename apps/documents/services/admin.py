from apps.documents.models import DocumentManagement, Document
from apps.documents.enums import BOUGHT
from django.utils.timezone import localtime
from apps.users.choices import MANAGER


class DocumentAdminService:
    def __init__(self, user):
        self.user = user

    def update_document_sale_status(self, documents, sale_status):
        DocumentManagement.objects.filter(
            user=self.user, document__in=documents
        ).update(sale_status=sale_status, last_update=localtime())


def prepare_doc_to_create(document: Document, users):
    return [
        DocumentManagement(document=document, user=user, sale_status=BOUGHT)
        if user.role == MANAGER
        else DocumentManagement(document=document, user=user)
        for user in users
    ]


def init_doc_mngt(document: Document, users):
    return DocumentManagement.objects.bulk_create(prepare_doc_to_create(document, users))
