from django.contrib import admin
from django.db.models import F
from django.utils.timezone import localtime

from apps.payment.models import Order
from apps.payment.enums import SUCCESS, FAILED
from apps.documents.models import DocumentManagement
from apps.documents import enums as doc_enums
from apps.courses.models import CourseManagement
from apps.courses import enums as course_enums



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # search_fields = (
    #     "user__first_name",
    # )
    list_display = (
        "code",
        "user",
        "total_price",
        "status",
        "created",
    )

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if change:
            if obj.status == SUCCESS:
                obj.documents.all().update(sold=F('sold') + 1)
                DocumentManagement.objects.filter(
                    user=obj.user, document__in=obj.documents.all()
                ).update(sale_status=doc_enums.BOUGHT, last_update=localtime())

                obj.courses.all().update(sold=F('sold') + 1)
                CourseManagement.objects.filter(
                    user=obj.user, course__in=obj.courses.all()
                ).update(sale_status=course_enums.BOUGHT, last_update=localtime())

            if obj.status == FAILED:
                DocumentManagement.objects.filter(
                    user=obj.user, document__in=obj.documents.all()
                ).update(sale_status=doc_enums.AVAILABLE, last_update=localtime())
                CourseManagement.objects.filter(
                    user=obj.user, course__in=obj.courses.all()
                ).update(sale_status=course_enums.AVAILABLE, last_update=localtime())
        obj.save()
