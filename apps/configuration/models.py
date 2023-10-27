import uuid

from django.db import models


class Configuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_time_limit = models.PositiveSmallIntegerField(null=True, blank=True, help_text="(hours)")
    unlimited_document_time = models.BooleanField(default=False)
    ip_address_limit = models.PositiveSmallIntegerField(default=3)
    unlimited_ip_addresses = models.BooleanField(default=False)
    user_tracking = models.BooleanField(default=False)
    tracking_views = models.BooleanField(default=False)
    display_mark = models.BooleanField(default=True)
    display_correct_answer = models.BooleanField(default=True)


class PersonalInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    method = models.CharField(max_length=50, null=True, blank=True)
    payment_info = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Payment Info"
        verbose_name_plural = "Payment Info"
