# Manual generate

from django.db import migrations
from math import ceil


def calculate_size(apps, schema_editor):
    UploadFile = apps.get_model("upload", "UploadFile")
    UploadVideo = apps.get_model("upload", "UploadVideo")
    UploadImage = apps.get_model("upload", "UploadImage")

    files = []
    videos = []
    images = []
    for obj in UploadFile.objects.all():
        try:
            obj.file_size = ceil(obj.file_path.size / 1024)
            files.append(obj)
        except Exception:
            obj.delete()

    for obj in UploadVideo.objects.all():
        try:
            obj.video_size = ceil(obj.video_path.size / 1024)
            videos.append(obj)
        except Exception:
            obj.delete()

    for obj in UploadImage.objects.all():
        try:
            obj.image_size = ceil(obj.image_path.size / 1024)
            images.append(obj)
        except Exception:
            obj.delete()

    if files:
        UploadFile.objects.bulk_update(files, fields=["file_size"])
    if videos:
        UploadVideo.objects.bulk_update(videos, fields=["video_size"])
    if images:
        UploadImage.objects.bulk_update(images, fields=["image_size"])


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0018_rename_user_embedded_url_uploadvideo_use_embedded_url'),
    ]

    operations = [
        migrations.RunPython(calculate_size)
    ]
