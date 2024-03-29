import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.users.models import User
from apps.courses.models import Course


class ReplyComment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.user.full_name} - {self.user.email}" if self.user else str(self.id)


class Comment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    reply_comments = models.ManyToManyField(ReplyComment, blank=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.course.name if self.course else ''}" if self.user else str(self.id)






