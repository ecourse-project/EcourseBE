import uuid

from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class Configuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_time_limit = models.PositiveSmallIntegerField(null=True, blank=True, help_text="(hours)")
    document_unlimited_time = models.BooleanField(default=False)


class PersonalInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    method = models.CharField(max_length=50, null=True, blank=True)
    payment_info = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Payment Info"
        verbose_name_plural = "Payment Info"
