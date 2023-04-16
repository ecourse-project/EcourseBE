from django.contrib import admin
from django.db.models import Q

from apps.documents.models import Document, DocumentManagement, DocumentTopic
from apps.documents.enums import AVAILABLE, IN_CART

from apps.upload.enums import video_ext_list
from apps.upload.models import UploadFile

from apps.upload.services.services import UploadCourseServices


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_filter = ("is_selling",)
    search_fields = (
        "name",
    )
    list_display = (
        "name",
        "topic",
        # "description",
        "thumbnail",
        "file",
        "price",
        "is_selling",
        "id",
        # "rating",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("sold", "views", "num_of_rates", "rating")

    # def save_model(self, request, obj, form, change):
    #     obj.save()

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


@admin.register(DocumentTopic)
class DocumentTopicAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    list_display = (
        "name",
    )


@admin.register(DocumentManagement)
class DocumentManagementAdmin(admin.ModelAdmin):
    list_filter = ("document", "user", "sale_status")
    search_fields = (
        "document__name",
        "user__email",
        "sale_status",
    )
    list_display = (
        "user",
        "document",
        "sale_status",
    )
