from django.contrib import admin
from apps.documents.models import Document, DocumentManagement
from apps.documents.enums import AVAILABLE, IN_CART


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
        if not Document.objects.filter(id=obj.id).exists():
            DocumentManagement.objects.bulk_create([
                DocumentManagement(document=obj, sale_status=AVAILABLE, user_id=user)
                for user in
                DocumentManagement.objects.order_by('user_id').values_list('user_id', flat=True).distinct('user_id')
            ])
        obj.save()

    def delete_model(self, request, obj):
        DocumentManagement.objects.filter(document=obj, sale_status__in=[AVAILABLE, IN_CART]).delete()
        obj.delete()



