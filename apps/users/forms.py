from django.contrib.auth.models import Permission
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from apps.core.general.enums import USER_PERMISSION_DISPLAY
from apps.users.models import User


class UserForm(forms.ModelForm):
    permissions = forms.MultipleChoiceField(
        required=False,
        widget=FilteredSelectMultiple('Permissions', False)
    )

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields["permissions"].choices = [(key, val) for key, val in USER_PERMISSION_DISPLAY.items()]

            instance_permission = self.instance.user_permissions.all()
            self.initial["permissions"] = [permission.codename for permission in instance_permission]
