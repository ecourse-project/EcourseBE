import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.courses.models import Course
from apps.users.models import User
from apps.upload.models import UploadImage

from ckeditor_uploader.fields import RichTextUploadingField


class PostTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    topic = models.ForeignKey(PostTopic, on_delete=models.SET_NULL, null=True, blank=True)
    header = models.CharField(max_length=20, null=True, blank=True)
    thumbnail = models.ForeignKey(UploadImage, related_name="posts", on_delete=models.SET_NULL, null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    content_summary = models.TextField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["views"]

    def __str__(self):
        return self.name
