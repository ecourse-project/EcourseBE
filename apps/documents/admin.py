from django.contrib import admin
from django.db.models import Q

from apps.documents.models import Document, DocumentManagement
from apps.documents.enums import AVAILABLE, IN_CART
from apps.documents.services.admin import init_doc_mngt
from apps.rating.models import DocumentRating
from apps.users.services import get_active_users
from apps.upload.enums import video_ext_list
from apps.upload.models import UploadFile


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    list_display = (
        "name",
        "description",
        "title",
        "thumbnail",
        "file",
        "is_selling",
        "rating",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("sold", "views")

    def save_model(self, request, obj, form, change):
        """ Init document data """
        if not Document.objects.filter(id=obj.id).exists():
            users = get_active_users()
            if users.count() > 0:
                init_doc_mngt(obj, users)
        obj.save()

        """ Init document rating """
        rating, _ = DocumentRating.objects.get_or_create(document=obj)

    def delete_model(self, request, obj):
        DocumentManagement.objects.filter(document=obj, sale_status__in=[AVAILABLE, IN_CART]).delete()
        obj.delete()

    def get_form(self, request, obj=None, **kwargs):
        form = super(DocumentAdmin, self).get_form(request, obj, **kwargs)
        q_list = Q()
        for q in [Q(file_type__iexact=ext) for ext in video_ext_list]:
            q_list |= q
        form.base_fields['file'].queryset = UploadFile.objects.filter(~q_list)
        return form



