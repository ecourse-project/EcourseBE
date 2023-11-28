from django.db.models import Q

from apps.users.choices import MANAGER


class AdminQuizPermissons:
    def __init__(self, user):
        self.user = user

    def user_condition(self, filter_field="author"):
        return (
            Q(**{filter_field: self.user})
            if not self.user.is_superuser and not self.user.role == MANAGER
            else Q()
        )

    def question_mngt_user_condition(self):
        return (
            Q(
                Q(choices_question__isnull=False, choices_question__author=self.user)
                | Q(match_question__isnull=False, match_question__author=self.user)
                | Q(fill_blank_question__isnull=False, fill_blank_question__author=self.user)
            )
            if not self.user.is_superuser and not self.user.role == MANAGER
            else Q()
        )
