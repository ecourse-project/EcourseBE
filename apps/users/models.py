import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django_better_admin_arrayfield.models.fields import ArrayField
from model_utils.models import TimeStampedModel

from apps.core.utils import get_media_url
from apps.users.choices import ROLE_CHOICES, DEVICE_TYPE, STUDENT


class User(AbstractUser):
    username = models.CharField(max_length=10, default="ecourse")
    first_name = None
    last_name = None
    is_staff = models.BooleanField(
        verbose_name="Admin Permission",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(null=True, blank=True, max_length=1000)
    phone = models.CharField(default="", blank=True, max_length=30)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=STUDENT)
    quiz_permission = models.BooleanField(default=False)
    ip_addresses = ArrayField(models.CharField(max_length=15), null=True, blank=True)  # Verified
    unverified_ip_addresses = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    is_testing_user = models.BooleanField(default=False)
    first_login = models.DateTimeField(blank=True, null=True)
    other_data = models.JSONField(default=dict(), null=True, blank=True)


    def __str__(self):
        return self.email

    def get_avatar(self):
        if self.avatar:
            return get_media_url(self.avatar)
        return None

    class Meta:
        ordering = ["full_name", "email"]


class UserDataBackUp(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    documents = models.JSONField(null=True, blank=True)
    courses = models.JSONField(null=True, blank=True)


class TestUser(User):
    class Meta:
        proxy = True
        verbose_name = "user"
        verbose_name_plural = "Test Users"


class UserResetPassword(models.Model):
    email = models.CharField(max_length=100)
    password_reset = models.CharField(max_length=1000, null=True, blank=True)
    is_changed = models.BooleanField(default=True)


class UserTracking(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    method = models.CharField(max_length=10, null=True, blank=True)
    ip_address = models.CharField(max_length=15, null=True, blank=True)
    path = models.CharField(max_length=100, null=True, blank=True)
    query_params = models.JSONField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "API tracking"
        verbose_name = "Object"


class DeviceTracking(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE, null=True, blank=True)
    device = models.CharField(max_length=20, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    browser_version = models.CharField(max_length=20, null=True, blank=True)
    system = models.CharField(max_length=50, null=True, blank=True)
    system_version = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Device tracking"
        verbose_name = "Object"


class CustomGroup(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    permissions = ArrayField(models.CharField(max_length=50), null=True, blank=True)

    class Meta:
        verbose_name_plural = "Permission Groups"
        verbose_name = "Group"
