from django.contrib.auth.models import Permission
from django.contrib import admin
from django.db.models import Q
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from apps.users.forms import UserForm
from apps.users.models import *
from apps.users.choices import MANAGER
from apps.core.utils import id_generator
from apps.core.general.backup import change_user_role
from apps.core.general.admin_site import get_admin_attrs


@admin.register(UserDataBackUp)
class UserDataBackUpAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        'user',
    )


@admin.register(TestUser)
class TestUserAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        'email',
        'full_name',
        'phone',
    )

    def get_fields(self, request, obj=None):
        fields = super(TestUserAdmin, self).get_fields(request, obj)
        for field in ["groups", "user_permissions"]:
            fields.remove(field)
        return fields

    def get_queryset(self, request):
        return super(TestUserAdmin, self).get_queryset(request).filter(
            Q(is_testing_user=True)
        )

    def save_model(self, request, obj, form, change):
        obj.save()
        change_user_role(obj, form.initial["role"], obj.role)


@admin.register(User)
class UserAdmin(admin.ModelAdmin, DynamicArrayMixin):
    form = UserForm
    filter_horizontal = ("user_permissions",)

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "User", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "User", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "User", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "User", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "User", "list_display")

    def get_queryset(self, request):
        qs = Q(is_testing_user=True)
        if not request.user.is_superuser:
            qs |= Q(is_superuser=True)
            qs |= Q(role=MANAGER) if not request.user.role == MANAGER else Q()
        return (
            super(UserAdmin, self)
            .get_queryset(request)
            .filter(~qs)
        )

    def save_model(self, request, obj, form, change):
        obj.save()
        change_user_role(obj, form.initial["role"], obj.role)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        permissions = form.cleaned_data.get("permissions")
        permission_objs = Permission.objects.filter(codename__in=permissions)
        instance.user_permissions.set(permission_objs)

    def has_add_permission(self, request):
        return get_admin_attrs(request, "User", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "User", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "User", "has_delete_permission")


@admin.register(UserResetPassword)
class UserResetPasswordAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'password_reset',
        'is_changed',
    )
    readonly_fields = ('password_reset', 'is_changed')

    def save_model(self, request, obj, form, change):
        email = obj.email.strip()
        user = User.objects.filter(email=email).first()
        if user:
            new_password = id_generator()
            user.set_password(new_password)
            user.save(update_fields=["password"])
            obj.password_reset = new_password
        obj.save()
        UserResetPassword.objects.filter(email=email).update(is_changed=False)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserTracking)
class UserTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'path',
        'created',
    )


@admin.register(DeviceTracking)
class DeviceTrackingAdmin(admin.ModelAdmin):
    search_fields = (
        "user__email",
        "user__full_name",
    )
    list_display = (
        "user",
        "device",
        "browser",
        "created",
    )
    fields = (
        "created",
        "user",
        "device_type",
        "device",
        "browser",
        "browser_version",
        "system",
        "system_version",
    )
    readonly_fields = ("created",)

    def get_queryset(self, request):
        return super(DeviceTrackingAdmin, self).get_queryset(request).select_related("user")
