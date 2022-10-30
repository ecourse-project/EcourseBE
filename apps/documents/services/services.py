from django.utils.timezone import localtime
from django.db.models import Prefetch, Q

from apps.documents.models import DocumentManagement, Document
from apps.documents.api.serializers import DocumentSerializer
from apps.documents.enums import BOUGHT, PENDING
from apps.rating.api.serializers import RatingSerializer
from apps.rating.models import DocumentRating


class DocumentService:
    def __init__(self, user):
        self.user = user

    @property
    def get_all_documents_queryset(self):
        return Document.objects.select_related('thumbnail', 'file')

    # Not used
    def get_documents_sale_status(self, documents) -> list:
        return list(map(lambda item: dict(item[0], sale_status=item[1]),
                        zip(DocumentSerializer(documents, many=True).data,
                            DocumentManagement.objects.filter(user=self.user, document__in=documents)
                            .order_by("document__name")
                            .values_list('sale_status', flat=True))))


class DocumentManagementService:
    def __init__(self, user):
        self.user = user

    @property
    def get_doc_management_queryset(self):
        return DocumentManagement.objects.prefetch_related(
            Prefetch('document', queryset=Document.objects.select_related(
                'thumbnail', 'file'))
        ).filter(user=self.user)

    def init_documents_management(self):
        if not DocumentManagement.objects.filter(user=self.user).first():
            DocumentManagement.objects.bulk_create([
                DocumentManagement(
                    user=self.user, last_update=localtime(), document=doc
                ) for doc in DocumentService(self.user).get_all_documents_queryset
            ])

    @property
    def get_doc_mngt_queryset_by_selling(self):
        query = Q(document__is_selling=True)
        query |= Q(document__is_selling=False) & Q(sale_status__in=[BOUGHT, PENDING])
        return self.get_doc_management_queryset.filter(query)

    def custom_doc_detail_data(self, data):
        document_rating = DocumentRating.objects.filter(document_id=data['id']).first()
        all_ratings = document_rating.ratings.all()
        my_rating = document_rating.ratings.filter(user=self.user).first()
        data['rating_detail'] = RatingSerializer(all_ratings, many=True).data if all_ratings else []
        data['my_rating'] = RatingSerializer(my_rating).data if my_rating else {}
        return data
