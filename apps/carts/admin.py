from django.contrib import admin
from apps.carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "user__full_name")
    list_display = (
        "user",
        "total_price",
    )
