from django.contrib import admin
from django.db.models import F
from django.utils.timezone import localtime

from apps.payment.models import Order
from apps.payment.enums import SUCCESS, FAILED
from apps.documents.models import DocumentManagement
from apps.documents import enums as doc_enums
from apps.documents.services.admin import DocumentAdminService
from apps.courses.models import CourseManagement
from apps.courses import enums as course_enums
from apps.courses.services.admin import CourseAdminService


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ("user", "status")
    search_fields = (
        "user__email",
    )
    list_display = (
        "code",
        "user",
        "total_price",
        "status",
        "created",
    )

    def has_delete_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if change:
            doc_service = DocumentAdminService(obj.user)
            course_service = CourseAdminService(obj.user)
            if obj.status == SUCCESS:
                """ Document """
                all_docs = obj.documents.all()
                all_docs.update(sold=F('sold') + 1)
                doc_service.update_document_sale_status(all_docs, doc_enums.BOUGHT)

                """ Course """
                all_courses = obj.courses.all()
                all_courses.update(sold=F('sold') + 1)
                course_service.update_course_sale_status(all_courses, course_enums.BOUGHT)
                course_service.init_courses_data(all_courses)

            if obj.status == FAILED:
                """ Document """
                doc_service.update_document_sale_status(obj.documents.all(), doc_enums.AVAILABLE)

                """ Course """
                all_courses = obj.courses.all()
                course_service.update_course_sale_status(all_courses, course_enums.AVAILABLE)
                course_service.disable_courses_data(all_courses)

        obj.save()

    def get_queryset(self, request):
        return super(OrderAdmin, self).get_queryset(request).select_related("user")
