from django.contrib import admin


@admin.action(description='Enable for selected records')
def enable(modeladmin, request, queryset):
    queryset.update(enable=True)


@admin.action(description='Disable for selected records')
def disable(modeladmin, request, queryset):
    queryset.update(enable=False)


@admin.action(description='Unremove for selected lessons')
def unremove(modeladmin, request, queryset):
    queryset.update(removed=False)
