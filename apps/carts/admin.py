from django.contrib import admin
from apps.carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "user__full_name")
    list_display = (
        "user",
        "total_price",
    )

    def get_queryset(self, request):
        return super(CartAdmin, self).get_queryset(request).select_related("user")
