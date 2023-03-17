import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.documents.models import DocumentTopic, Document
from apps.courses.models import CourseTopic, Course
from django_better_admin_arrayfield.models.fields import ArrayField


class Header(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True, blank=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class HeaderDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    document_topic = models.ForeignKey(DocumentTopic, null=True, blank=True, on_delete=models.CASCADE)
    course_topic = models.ForeignKey(CourseTopic, null=True, blank=True, on_delete=models.CASCADE)
    header = models.ForeignKey(Header, null=True, blank=True, related_name="header_detail", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=1)


class HomePageDetail(models.Model):
    display_name = models.CharField(max_length=100, null=True, blank=True)
    documents = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    courses = ArrayField(models.CharField(max_length=50), null=True, blank=True)

