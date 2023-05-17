import os
import shutil

from django.core.files.storage import default_storage
from django.conf import settings

from apps.upload.services.storage.base import get_file_path
from apps.upload.models import UploadFile, UploadImage, UploadVideo
from apps.upload.enums import FILE, IMAGE, VIDEO


def get_user(request):
    user = request.user
    return None if user.is_anonymous else user


def upload_files(request, files, folder_name: str = None):
    upload_file_list = []
    for file in files:
        file_path = get_file_path(folder_name, file.name)
        default_storage.save(file_path, file)
        upload_file_list.append(
            UploadFile(
                file_path=file_path,
                file_size=file.size,
                file_type=file.name.split(".")[-1],
                user=get_user(request),
            )
        )
    created = UploadFile.objects.bulk_create(upload_file_list)
    return created


def upload_images(request, images, folder_name: str = None):
    upload_image_list = []
    for image in images:
        image_path = get_file_path(image.name, folder_name)
        default_storage.save(image_path, image)
        upload_image_list.append(
            UploadImage(
                image_path=image_path,
                image_size=image.size,
                image_type=image.name.split(".")[-1],
                user=get_user(request),
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
    destination_dir = destination_dir.replace(chr(92), "/").replace("media", "").strip("/")

    new_path = "/".join([root, destination_dir])
    file_name = os.path.basename(source_file)
    save_path = "/".join([destination_dir, file_name])

    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    shutil.move("/".join([root, source_file]), new_path)

    if upload_type.lower() == IMAGE:
        UploadImage.objects.filter(image_path=source_file).update(image_path=save_path)
    elif upload_type.lower() == VIDEO:
        UploadVideo.objects.filter(video_path=source_file).update(video_path=save_path)
    else:
        UploadFile.objects.filter(file_path=source_file).update(file_path=save_path)


