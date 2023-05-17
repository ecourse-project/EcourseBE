from math import ceil
from datetime import datetime
import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage

from ckeditor_uploader.utils import storage
from moviepy.editor import VideoFileClip

from apps.upload.enums import FILE, IMAGE, VIDEO, video_ext_list


def get_file_path(file_name, new_file_name="default", folder_name=None, upload_type=FILE):
    file_name_split = os.path.splitext(file_name)
    file_ext = file_name_split[1] or ""
    if file_ext.replace(".", "").lower() == settings.DEFAULT_CMD_FILE_EXT:
        return f"commands/{file_name}.py", "py"

    upload_type += "s"
    date_now = datetime.now()
    if not folder_name:
        folder = "/".join([str(date_now.year), f"{date_now:%m}", f"{date_now:%d}", upload_type])
    else:
        folder = "/".join([folder_name, str(date_now.year), f"{date_now:%m}", f"{date_now:%d}", upload_type])

    return f"{folder}/{new_file_name}{file_ext}", file_ext.replace(".", "").lower()


def store_file_upload(upload_obj, upload_path, upload_type):
    save_path, file_ext = get_file_path(file_name=upload_path.name, new_file_name=upload_obj.id, upload_type=upload_type)
    default_storage.save(save_path, upload_path)

    if not save_path.startswith("commands"):
        if upload_type.lower() == IMAGE:
            upload_obj.image_path = save_path
            upload_obj.image_size = ceil(upload_obj.image_path.size / 1024)
            upload_obj.image_type = file_ext or None
        elif upload_type.lower() == VIDEO:
            upload_obj.video_path = save_path
            upload_obj.video_size = ceil(upload_obj.video_path.size / 1024)
            upload_obj.video_type = file_ext or None
            if file_ext and file_ext.upper() in video_ext_list:
                upload_obj.duration = VideoFileClip(upload_obj.video_path.path).duration
        else:
            upload_obj.file_path = save_path
            upload_obj.file_size = ceil(upload_obj.file_path.size / 1024)
            upload_obj.file_type = file_ext or None


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
