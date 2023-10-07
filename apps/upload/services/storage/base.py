import os
import uuid
from math import ceil
from datetime import datetime
import zipfile

from django.conf import settings
from django.core.files.storage import default_storage

from ckeditor_uploader.utils import storage
from moviepy.editor import VideoFileClip

from apps.core.utils import get_default_hidden_file_type, generate_file_name_by_id, get_file_name_or_ext
from apps.upload.enums import FILE, IMAGE, VIDEO, DIR, video_ext_list


def get_folder_name(folder_name, upload_type):
    date_now = datetime.now()
    if not folder_name:
        return "/".join([str(date_now.year), f"{date_now:%m}", f"{date_now:%d}", upload_type])
    else:
        return "/".join([folder_name, str(date_now.year), f"{date_now:%m}", f"{date_now:%d}", upload_type])


def get_file_path(file_name, new_file_name="default", folder_name=None, upload_type=FILE):
    file_ext = get_file_name_or_ext(filename=file_name, get_name=False)
    if file_ext.replace(".", "").lower() in get_default_hidden_file_type():
        return f"hidden/{file_name}", file_ext.replace(".", "").lower()

    folder = get_folder_name(folder_name, f"{upload_type}s")
    return f"{folder}/{new_file_name}{file_ext}", file_ext.replace(".", "").lower()


def store_file_upload(upload_obj, upload_path, upload_type):
    save_path, file_ext = get_file_path(
        file_name=upload_path.name,
        new_file_name=generate_file_name_by_id(str(upload_obj.id)),
        upload_type=upload_type,
    )

    default_storage.save(save_path, upload_path)

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


def upload_and_unzip_folder(upload_path, object_id):
    storage_folder = f"{get_folder_name(None, DIR)}/{str(object_id)}"
    with zipfile.ZipFile(upload_path, 'r') as zip_ref:
        zip_ref.extractall(f"{settings.MEDIA_ROOT}/{storage_folder}")
