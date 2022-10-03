from django.core.files.storage import default_storage
from rest_framework.request import Request
from apps.upload.exceptions import FileEmptyException
from apps.upload.services.storage.base import get_file_path
from apps.upload.models import UploadFile, UploadImage


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
