from apps.upload.exceptions import FolderNameEmptyException
from datetime import datetime
from os import path


def get_file_path(file_name, folder_name=None):
    date_now = datetime.now()
    if not folder_name:
        folder = "/".join([str(date_now.year), f"{date_now:%m}", f"{date_now:%d}"])
    else:
        folder = "/".join([folder_name, str(date_now.year), f"{date_now:%m}", f"{date_now:%d}"])
    path_url = [folder, file_name]
    return path.join(*path_url)
