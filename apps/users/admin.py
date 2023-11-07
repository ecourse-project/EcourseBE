from django.contrib import admin
from django.db.models import Q
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from apps.users.models import *
from apps.users.choices import MANAGER
from apps.core.utils import id_generator
from apps.core.general.backup import change_user_role


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
    search_fields = ("email", "full_name", "phone")
    list_display = (
        "email",
        "full_name",
        "phone",
        "last_login",
        "date_joined",
    )
    fields = [
        "email",
        "full_name",
        "avatar",
        "phone",
        "role",
        "first_login",
        "last_login",
        "date_joined",
        "ip_addresses",
        "unverified_ip_addresses",
        "other_data",
        "is_superuser",
        "is_staff",
        "is_active",
        "is_testing_user",
        "user_permissions",
    ]

    filter_horizontal = ("user_permissions",)
    readonly_fields = ("first_login", "last_login", "date_joined")

    def get_fields(self, request, obj=None):
        user = request.user
        fields = super(UserAdmin, self).get_fields(request, obj)

        removed_fields = []
        if not user.is_superuser:
            removed_fields.extend(["is_superuser", "other_data"])
            if not user.role == MANAGER:
                removed_fields.extend(["user_permissions", "is_staff", "role", "is_testing_user"])

        for field in removed_fields:
            if field in fields:
                fields.remove(field)
        return fields

    def get_queryset(self, request):
        qs = Q(is_testing_user=True)
        if not request.user.is_superuser:
            qs |= Q(is_superuser=True)
            if not request.user.role == MANAGER:
                qs |= Q(role=MANAGER) | Q(email="admin@admin.com")
        return super(UserAdmin, self).get_queryset(request).filter(~qs)

    def save_model(self, request, obj, form, change):
        obj.save()
        change_user_role(obj, form.initial["role"], obj.role)


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
