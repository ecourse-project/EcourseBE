import uuid

from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models
from model_utils.models import TimeStampedModel

from apps.documents.models import DocumentTopic
from apps.courses.models import CourseTopic
from apps.core.general.enums import DATA_TYPE_CHOICES
from apps.posts.models import PostTopic


class Header(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES, null=True, blank=True)
    order = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.display_name if self.display_name else "Header's display name - None"


class HeaderDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    header = models.ForeignKey(Header, null=True, blank=True, related_name="header_detail", on_delete=models.SET_NULL)
    document_topic = models.ForeignKey(DocumentTopic, null=True, blank=True, on_delete=models.SET_NULL)
    course_and_class_topic = models.ForeignKey(CourseTopic, null=True, blank=True, on_delete=models.SET_NULL)
    post_topic = models.ForeignKey(PostTopic, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["header", "order"]

    def __str__(self):
        return self.display_name if self.display_name else "Header detail's display name - None"


class HomePageDetail(models.Model):
    display_name = models.CharField(max_length=100, null=True, blank=True)
    max_items_display = models.PositiveSmallIntegerField(default=6)
    documents = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    courses = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    classes = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    posts = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order', "display_name"]

    def __str__(self):
        return self.display_name if self.display_name else "Homepage's display name - None"

