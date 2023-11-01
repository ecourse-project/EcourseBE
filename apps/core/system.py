import os
from pprint import pformat


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
