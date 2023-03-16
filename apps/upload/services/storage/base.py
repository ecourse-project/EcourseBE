from datetime import datetime
import os


def get_file_path(file_name, new_file_name="default", folder_name=None):
    date_now = datetime.now()
    if not folder_name:
        folder = "/".join([str(date_now.year), f"{date_now:%m}", f"{date_now:%d}"])
    else:
        folder = "/".join([folder_name, str(date_now.year), f"{date_now:%m}", f"{date_now:%d}"])
    file_name_split = os.path.splitext(file_name)
    file_ext = file_name_split[1] or ""
    return f"{folder}/{new_file_name}{file_ext}", file_ext.replace(".", "")
