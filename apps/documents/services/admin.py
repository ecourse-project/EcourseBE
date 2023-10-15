from apps.documents.models import DocumentManagement


class DocumentAdminService:
    def __init__(self, user):
        self.user = user

    def update_document_sale_status(self, documents, sale_status):
        DocumentManagement.objects.filter(
            user=self.user, document__in=documents
        ).update(sale_status=sale_status)
