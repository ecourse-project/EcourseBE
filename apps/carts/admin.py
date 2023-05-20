from django.contrib import admin
from apps.carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_filter = ("user",)
    search_fields = ("user__email",)
    list_display = (
        "user",
        "total_price",
    )
