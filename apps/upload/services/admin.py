from django.db.models import Q
from apps.users.choices import MANAGER


class AdminUploadPermissons:
    def __init__(self, user):
        self.user = user

    def user_condition(self):
        return (
            Q(author=self.user)
            if not self.user.is_superuser and not self.user.role == MANAGER
            else Q()
        )
