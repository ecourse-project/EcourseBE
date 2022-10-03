import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from apps.core.utils import get_media_url


class User(AbstractUser):
    username = models.CharField(max_length=10, default="ecourse")
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(null=True, blank=True, max_length=1000)
    phone = models.CharField(default="", blank=True, max_length=30)

    def __str__(self):
        return self.full_name

    def get_avatar(self):
        if self.avatar:
            return get_media_url(self.avatar)
        return None
