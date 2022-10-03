from django.db.models import Prefetch

from apps.comments.models import Comment, ReplyComment


def get_comments_queryset():
    return Comment.objects.prefetch_related(
        Prefetch("reply_comments", queryset=ReplyComment.objects.select_related("user"))
    ).select_related("user", "course")
