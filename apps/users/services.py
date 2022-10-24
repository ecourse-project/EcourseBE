from apps.users.exceptions import MissedUsernameOrEmailException
from apps.users.models import User


def exists_user(**kwargs):
    if not any(i for i in kwargs.values()):
        raise MissedUsernameOrEmailException()
    count = User.objects.filter(**{f"{field}__iexact": val for field, val in kwargs.items() if val}).count()
    return count > 0


def get_active_users():
    return User.objects.filter(is_active=True, is_superuser=False, last_login__isnull=False)
