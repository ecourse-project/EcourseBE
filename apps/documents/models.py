import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.upload.models import UploadFile, UploadImage
from apps.users.models import User
from apps.documents.enums import STATUSES, AVAILABLE


class DocumentTitle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Document(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    title = models.ForeignKey(DocumentTitle, null=True, blank=True, related_name="docs", on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    thumbnail = models.ForeignKey(
        UploadImage, related_name="documents", on_delete=models.CASCADE, null=True, blank=True,
    )
    file = models.ForeignKey(
        UploadFile, related_name="documents", on_delete=models.CASCADE, null=True, blank=True,
    )
    is_selling = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    num_of_rates = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DocumentManagement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="doc_mngt", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    sale_status = models.CharField(max_length=15, choices=STATUSES, default=AVAILABLE)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ["document__name"]

    def __str__(self):
        return f"{self.document.name} - {self.user.__str__()}"



