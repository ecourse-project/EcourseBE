import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.documents.models import DocumentTitle
from apps.courses.models import CourseTitle


class Header(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True, blank=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class HeaderDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    document_title = models.ForeignKey(DocumentTitle, null=True, blank=True, on_delete=models.CASCADE)
    course_title = models.ForeignKey(CourseTitle, null=True, blank=True, on_delete=models.CASCADE)
    header = models.ForeignKey(Header, null=True, blank=True, related_name="header_detail", on_delete=models.CASCADE)
