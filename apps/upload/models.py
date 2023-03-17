import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.users.models import User


class UploadFile(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_path = models.FileField(max_length=128, null=True, blank=True)
    file_size = models.PositiveBigIntegerField(null=True, help_text="(KB)")
    file_type = models.CharField(max_length=10, null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, help_text=("Seconds"))

    def __str__(self):
        return str(self.file_name)

    def delete_file(self):
        self.file_path.delete()

    def delete(self, *args, **kwargs):
        self.delete_file()
        super().delete(*args, **kwargs)


class UploadImage(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_path = models.ImageField(max_length=128, null=True, blank=True)
    image_size = models.PositiveBigIntegerField(null=True, help_text="(KB)")
    image_type = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.image_path)

    def delete_image(self):
        self.image_path.delete()

    def delete(self, *args, **kwargs):
        self.delete_image()
        super().delete(*args, **kwargs)
