from django.contrib import admin

from apps.payment.models import Order
from apps.payment.enums import SUCCESS, FAILED
from apps.payment.services.services import OrderService


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

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

    def delete_model(self, request, obj):
        order_service = OrderService(obj)
        order_service.order_failed()
        obj.delete()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        order_service = OrderService(instance)

        if instance.status == SUCCESS:
            order_service.order_success()
        elif instance.status == FAILED:
            order_service.order_failed()

    def get_queryset(self, request):
        return super(OrderAdmin, self).get_queryset(request).select_related("user")
