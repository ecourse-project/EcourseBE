import os

from apps.upload.services.upload import move_file


def apply_dir_action(action: str, root: str, source: str, destination: str = "", file_type: str = ""):
    source_path = "/".join([root, source]).replace(chr(92), "/")
    des_path = "/".join([root, destination]).replace(chr(92), "/")
    message = f"{action} {source or source_path}"

    if action == "delete":
        try:
            if os.path.isdir(source_path):
                os.rmdir(source_path)
            else:
                os.remove(source_path)
            message = f"{source_path} is {action}d"
        except Exception:
            message = f"Cannot {action} {source_path}"
    elif action == "move":
        try:
            move_file(root, source, destination, file_type)
            message = f"{source_path} is {action}d -> {des_path}"
        except Exception:
            message = f"Cannot {action} {source_path}"
    elif action == "create folder":
        os.mkdir(source_path)

    return message


def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size
