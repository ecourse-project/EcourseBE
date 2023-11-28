import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.core.utils import get_summary_content
from apps.upload.enums import video_ext_list
from apps.users.models import User


class UploadFile(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_path = models.FileField(max_length=255, null=True, blank=True)
    file_size = models.PositiveBigIntegerField(null=True, help_text="(KB)")
    file_type = models.CharField(max_length=10, null=True, blank=True)
    ip_address = models.CharField(max_length=128, null=True, blank=True)
    file_embedded_url = models.TextField(null=True, blank=True)
    use_embedded_url = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["file_name"]

    def __str__(self):
        return get_summary_content(self.file_name)

    def delete_file(self):
        self.file_path.delete()

    def delete(self, *args, **kwargs):
        self.delete_file()
        super().delete(*args, **kwargs)


class UploadImage(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_name = models.CharField(max_length=255, null=True, blank=True)
    image_path = models.ImageField(max_length=255, null=True, blank=True)
    image_size = models.PositiveBigIntegerField(null=True, help_text="(KB)")
    image_type = models.CharField(max_length=10, null=True, blank=True)
    ip_address = models.CharField(max_length=128, null=True, blank=True)
    is_avatar = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["image_name"]

    def __str__(self):
        return get_summary_content(self.image_name)

    def delete_image(self):
        self.image_path.delete()

    def delete(self, *args, **kwargs):
        self.delete_image()
        super().delete(*args, **kwargs)


class UploadAvatar(UploadImage):
    class Meta:
        proxy = True
        verbose_name_plural = "User Avatar"


class UploadVideo(TimeStampedModel):
    @staticmethod
    def get_available_video_type():
        return " ".join([f".{ext.lower()}" for ext in video_ext_list])

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveSmallIntegerField(default=1)
    video_name = models.CharField(max_length=255, null=True, blank=True)
    video_path = (
        models.FileField(
            max_length=255, null=True, blank=True,
            help_text=f"(Support: {get_available_video_type()})",
        )
    )
    video_size = models.PositiveBigIntegerField(null=True, help_text="(KB)")
    video_type = models.CharField(max_length=10, null=True, blank=True)
    video_embedded_url = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True, help_text="Seconds")
    use_embedded_url = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=128, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return get_summary_content(self.video_name)

    def delete_video(self):
        self.video_path.delete()

    def delete(self, *args, **kwargs):
        self.delete_video()
        super().delete(*args, **kwargs)


class UploadFolder(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    folder_path = models.FileField(max_length=255, null=True, blank=True, help_text="(.zip file)")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return get_summary_content(self.name)
