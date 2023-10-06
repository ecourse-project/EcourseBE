import os
import re
import functools
import random
import time
from typing import Union, List, Tuple, Text
from string import ascii_letters, digits

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import connection, reset_queries

from rest_framework.serializers import ModelSerializer


def is_absolute_url(url: str) -> bool:
    if re.match(r"^https?:\/\/", url):
        return True
    return False


def get_absolute_url(url: str, ) -> str:
    if is_absolute_url(url):
        return url

    base_url = str(settings.BASE_URL).rstrip("/")
    return f'{base_url}/{url.lstrip("/")}'


def get_media_url(file_path, from_root=False) -> str:
    if is_absolute_url(file_path):
        return file_path
    url = file_path.replace(str(settings.BASE_DIR), "") if from_root else default_storage.url(file_path.lstrip("/"))
    return get_absolute_url(url)


def get_media_url_from_root_path(file_path):
    if is_absolute_url(file_path):
        return file_path
    base_url = str(settings.BASE_URL).rstrip("/")


def id_generator(size=8, chars=ascii_letters + digits):
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for _ in range(size))


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function: " + func.__name__)
        print("Number of Queries: {}".format(end_queries - start_queries))
        print("Finished in: {}".format(end - start))

        return result

    return inner_func


def get_default_hidden_file_type():
    return [ext.strip() for ext in settings.DEFAULT_HIDDEN_FILE_EXT.split(",")]


def generate_file_name_by_id(obj_id):
    return ''.join(random.sample(obj_id, len(obj_id)))


def generate_random_character(n=10):
    return ''.join(random.choices(ascii_letters, k=n))


def create_serializer_class(model_class, fields: Union[List, Tuple, Text]):
    meta_class = type('Meta', (object,), {'model': model_class, 'fields': fields})
    return type(f'{meta_class}Serializer', (ModelSerializer,), {'Meta': meta_class})


def get_summary_content(content, max_word=10):
    if content and isinstance(content, str):
        content_elements = content.split(" ")
        summary = " ".join(content_elements[:max_word])
        return summary + "..." if len(content_elements) > max_word else summary
    return ""


def get_file_name_or_ext(filename, get_name=True):
    full_filename = os.path.basename(filename)
    name, ext = os.path.splitext(full_filename)
    return (name if get_name else ext) or ""


def get_file_from_nested_folder(dir_path):
    file_paths = []
    for folder, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(folder, file)
            file_paths.append(file_path)

    return file_paths
