import re
import functools
import random
import time
from string import ascii_letters, digits

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import connection, reset_queries


def is_absolute_url(url: str) -> bool:
    if re.match(r"^https?:\/\/", url):
        return True
    return False


def get_absolute_url(url: str) -> str:
    if is_absolute_url(url):
        return url

    base_url = str(settings.BASE_URL).rstrip("/")
    return f'{base_url}/{url.lstrip("/")}'


def get_media_url(file_path) -> str:
    if is_absolute_url(file_path):
        return file_path
    url = default_storage.url(file_path.lstrip("/"))
    return get_absolute_url(url)


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

        print("Function : " + func.__name__)
        print("Number of Queries : {}".format(end_queries - start_queries))
        print("Finished in : {}".format(end - start))

        return result

    return inner_func
