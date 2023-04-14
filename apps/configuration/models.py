import uuid

from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class Configuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_time_limit = models.PositiveSmallIntegerField(null=True, blank=True, help_text="(hours)")


class PersonalInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    payment_info = ArrayField(models.CharField(max_length=255), null=True, blank=True)
