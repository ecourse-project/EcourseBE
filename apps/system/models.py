import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.system.choices import STORAGE_CHOICES


class Storage(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    storage_type = models.CharField(max_length=20, choices=STORAGE_CHOICES, null=True, blank=True)
    size = models.PositiveBigIntegerField(default=0, help_text="(byte)")

    class Meta:
        ordering = ["-created"]


class SystemConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fe_dir_name = models.CharField(max_length=50, default="EcourseFE")
    be_dir_name = models.CharField(max_length=50, default="EcourseBE")
    data_file_name = models.CharField(max_length=100, default="exported_data.json")

