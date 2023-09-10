import os
import json
from pprint import pformat
import jwt

from django.conf import settings

from apps.users.models import UserTracking
from ipware import get_client_ip


def _get_dir_content(path, include_folders, recursive):
    entries = os.listdir(path)
    for entry in entries:
        entry_with_path = os.path.join(path, entry)
        if os.path.isdir(entry_with_path):
            if include_folders:
                yield entry_with_path
            if recursive:
                for sub_entry in _get_dir_content(entry_with_path, include_folders, recursive):
                    yield sub_entry
        else:
            yield entry_with_path


def get_dir_content(path, include_folders=True, recursive=True, prepend_folder_name=True):
    path_len = len(path) + len(os.path.sep)
    for item in _get_dir_content(path, include_folders, recursive):
        yield item if prepend_folder_name else item[path_len:]


def get_tree_str(path, indent=''):
    """Returns the folder tree starting at the given path as a string."""
    tree_str = indent + os.path.basename(path) + '\n'
    if os.path.isdir(path):
        for filename in os.listdir(path):
            tree_str += get_tree_str(os.path.join(path, filename), indent + '    ')
    return tree_str

# Example usage:
# tree_str = get_tree_str('/path/to/folder')


def tracking_user(request):
    user_id = None
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")

    post_data = request.body.decode('utf-8')
    try:
        data = json.loads(post_data)
    except Exception:
        data = None

    UserTracking.objects.create(
        user_id=user_id,
        method=request.method,
        ip_address=get_client_ip(request)[0],
        path=request.path,
        query_params=request.GET.dict() or None,
        data=data,
    )




