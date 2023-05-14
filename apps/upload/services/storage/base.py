from datetime import datetime
import os
import inspect
import warnings
import uuid

from django.conf import settings
from django.utils.module_loading import import_string

from ckeditor_uploader import utils
from ckeditor_uploader.utils import storage

from apps.upload.enums import FILE, IMAGE, VIDEO


def get_file_path(file_name, new_file_name="default", folder_name=None, upload_type=FILE):
    upload_type += "s"
    date_now = datetime.now()
    if not folder_name:
        folder = "/".join([str(date_now.year), f"{date_now:%m}", f"{date_now:%d}", upload_type])
    else:
        folder = "/".join([folder_name, str(date_now.year), f"{date_now:%m}", f"{date_now:%d}", upload_type])

    file_name_split = os.path.splitext(file_name)
    file_ext = file_name_split[1] or ""
    return f"{folder}/{new_file_name}{file_ext}", file_ext.replace(".", "").lower()


def get_user_path(user):
    user_path = ""

    # If CKEDITOR_RESTRICT_BY_USER is True upload file to user specific path.
    RESTRICT_BY_USER = getattr(settings, "CKEDITOR_RESTRICT_BY_USER", False)
    if RESTRICT_BY_USER:
        try:
            user_prop = getattr(user, RESTRICT_BY_USER)
        except (AttributeError, TypeError):
            user_prop = getattr(user, "get_username")

        if callable(user_prop):
            user_path = user_prop()
        else:
            user_path = user_prop

    return str(user_path)


def custom_get_upload_filename(upload_name, request):
    user_path = get_user_path(request.user)

    # Generate date based path to put uploaded file.
    # If CKEDITOR_RESTRICT_BY_DATE is True upload file to date specific path.
    if getattr(settings, "CKEDITOR_RESTRICT_BY_DATE", True):
        date_path = datetime.now().strftime("%Y/%m/%d")
    else:
        date_path = ""

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, user_path, date_path)

    file_name_split = os.path.splitext(upload_name)
    file_ext = file_name_split[1] or ""
    image_id = uuid.uuid4()  # New file name

    return (
        image_id,
        storage.get_available_name(os.path.join(upload_path, f"{IMAGE}s", f"{str(image_id)}{file_ext}")),
        file_ext.replace(".", "").lower(),
    )
