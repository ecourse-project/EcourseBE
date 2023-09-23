import os
import shutil
from math import ceil

from django.core.files.storage import default_storage

from apps.upload.services.storage.base import get_file_path
from apps.upload.models import UploadFile, UploadImage, UploadVideo
from apps.upload.enums import FILE, IMAGE, VIDEO
from apps.core.utils import generate_file_name_by_id, generate_random_character

from ipware.ip import get_client_ip


def get_user(request):
    user = request.user
    return None if user.is_anonymous else user


def generate_storage_image_name(user, is_avatar=False):
    user_id = generate_file_name_by_id(str(user.id)) if user else generate_random_character(20)
    user_email = user.email if user else "anonymous"
    image_name = f"{user_email}-{user_id}"

    if is_avatar:
        image_name = f"{image_name}-avatar"

    return image_name


def generate_instance_image_name(user, is_avatar=False, image_name=""):
    user_id = str(user.id) if user else ""
    user_email = user.email if user else "anonymous"

    if is_avatar:
        image_name = f"{user_email}-{user_id}".strip("-")

    return image_name


def upload_files(request, folder_name: str = None):
    upload_file_list = []
    files = request.FILES.getlist("file", [])
    for file in files:
        file_path, file_ext = get_file_path(file_name=file.name, folder_name=folder_name, upload_type=FILE)
        default_storage.save(file_path, file)
        upload_file_list.append(
            UploadFile(
                file_path=file_path,
                file_size=ceil(file.size / 1024),
                file_type=file_ext,
                ip_address=get_client_ip(request),
            )
        )
    created = UploadFile.objects.bulk_create(upload_file_list)
    return created


def upload_images(request, folder_name: str = None):
    user = get_user(request)
    is_avatar = request.data.get("is_avatar", False)

    upload_image_list = []
    images = request.FILES.getlist("image", [])
    for image in images:
        image_path, img_ext = get_file_path(
            file_name=image.name,
            new_file_name=generate_storage_image_name(user=user, is_avatar=is_avatar),
            folder_name=folder_name,
            upload_type=IMAGE,
        )
        default_storage.save(image_path, image)
        upload_image_list.append(
            UploadImage(
                image_name=generate_instance_image_name(user=user, is_avatar=is_avatar),
                image_path=image_path,
                image_size=ceil(image.size / 1024),
                image_type=img_ext,
                ip_address=get_client_ip(request),
                is_avatar=is_avatar,
            )
        )
    created = UploadImage.objects.bulk_create(upload_image_list)
    return created


def update_image(image_id, image, folder_name: str = None):
    image_path = get_file_path(folder_name, image.name)
    default_storage.save(image_path, image)
    instance = UploadImage.objects.get(id=image_id)
    instance.image_path = image_path
    instance.image_size = image.size
    instance.image_type = image.name.split(".")[-1]
    instance.save(update_fields=['image_path', 'image_size', 'image_type'])
    return instance


def update_file(file_id, file, folder_name: str = None):
    file_path = get_file_path(folder_name, file.name)
    default_storage.save(file_path, file)
    instance = UploadFile.objects.get(id=file_id)
    instance.file_path = file_path
    instance.file_size = file.size
    instance.file_type = file.name.split(".")[-1]
    instance.save(update_fields=['file_path', 'file_size', 'file_type'])
    return instance


def move_file(root: str, source_file: str, destination_dir: str, upload_type: str):
    if not (source_file and destination_dir and upload_type in [IMAGE, VIDEO, FILE]):
        return

    source_file = source_file.strip("/")
    destination_dir = destination_dir.replace(chr(92), "/").strip("/")

    old_path = "/".join([root, source_file])
    new_path = "/".join([root, destination_dir])

    file_name = os.path.basename(source_file)
    save_path = "/".join([destination_dir, file_name])

    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    shutil.move(old_path, new_path)

    source_file = source_file.replace("media", "").strip("/")
    if upload_type.lower() == IMAGE:
        UploadImage.objects.filter(image_path=source_file).update(image_path=save_path)
    elif upload_type.lower() == VIDEO:
        UploadVideo.objects.filter(video_path=source_file).update(video_path=save_path)
    else:
        UploadFile.objects.filter(file_path=source_file).update(file_path=save_path)
