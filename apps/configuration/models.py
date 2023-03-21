import uuid

from django.db import models


class Configuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_time_limit = models.PositiveSmallIntegerField(null=True, blank=True, help_text="(hours)")
