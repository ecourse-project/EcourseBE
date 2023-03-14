from django.contrib import admin

from apps.rating.models import DocumentRating, CourseRating, Rating
from apps.documents.enums import AVAILABLE, IN_CART


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rating",
        "created",
    )

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(DocumentRating)
class DocumentRatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
    )
    readonly_fields = ('ratings',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
    )
    readonly_fields = ('ratings',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
