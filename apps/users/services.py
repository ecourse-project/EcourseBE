from apps.users.exceptions import MissedUsernameOrEmailException
from apps.users.models import User


def exists_user(**kwargs):
    if not any(i for i in kwargs.values()):
        raise MissedUsernameOrEmailException()
    count = User.objects.filter(**{f"{field}__iexact": val for field, val in kwargs.items() if val}).count()
    return count > 0