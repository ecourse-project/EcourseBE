import uuid

from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models
from model_utils.models import TimeStampedModel

from apps.documents.models import DocumentTopic
from apps.courses.models import CourseTopic
from apps.classes.models import ClassTopic
from apps.posts.models import PostTopic


class Header(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.display_name


class HeaderDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    header = models.ForeignKey(Header, null=True, blank=True, related_name="header_detail", on_delete=models.SET_NULL)
    document_topic = models.ForeignKey(DocumentTopic, null=True, blank=True, on_delete=models.SET_NULL)
    course_topic = models.ForeignKey(CourseTopic, null=True, blank=True, on_delete=models.SET_NULL)
    class_topic = models.ForeignKey(ClassTopic, null=True, blank=True, on_delete=models.SET_NULL)
    post_topic = models.ForeignKey(PostTopic, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["header", "order"]


class HomePageDetail(models.Model):
    display_name = models.CharField(max_length=100, null=True, blank=True)
    documents = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    courses = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    classes = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    posts = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

