import os

from django.conf import settings
from apps.upload.enums import DIR


def find_dir_by_instance(instance):
    directory_path = "/".join([
        settings.MEDIA_ROOT.rstrip("/"),
        instance.created.strftime("%Y"),
        instance.created.strftime("%m"),
        instance.created.strftime("%d"),
        DIR,
        str(instance.pk),
    ])

    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return ""

    return directory_path
