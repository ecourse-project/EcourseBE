from django.contrib import admin
from apps.users.models import User, UserResetPassword
# from django.contrib.auth.admin import UserAdmin
from apps.core.utils import id_generator

admin.site.register(User)


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
