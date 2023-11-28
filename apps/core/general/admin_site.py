from apps.users.choices import MANAGER, TEACHER
from apps.core.general.enums import ADMIN_DISPLAY


def get_admin_attrs(request, model_name, admin_attr_name):
    user = request.user
    if user.is_superuser:
        return ADMIN_DISPLAY["SUPERUSER"][model_name][admin_attr_name]
    elif not user.is_superuser and user.role == MANAGER:
        return ADMIN_DISPLAY[MANAGER][model_name][admin_attr_name]
    return ADMIN_DISPLAY[TEACHER][model_name][admin_attr_name]


