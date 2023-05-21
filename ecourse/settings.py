"""
Django settings for ecourse project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
import environ
from django.core.management.commands.runserver import Command as runserver


env = environ.Env()
env.read_env()

runserver.default_port = env("PORT", default="8000")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = env("BASE_URL", default="http://be.creativeteaching.net")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0vv6d-m@%vjw60h8jxd42nb&pwi3t=t2pys3erjo^dbu6n(!q%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

INTERNAL_IPS = [
    '127.0.0.1'
]

# Application definition

LOCAL_APPS = [
    'apps.courses.apps.CoursesConfig',
    'apps.users.apps.UsersConfig',
    'apps.users_auth.apps.UsersAuthConfig',
    'apps.upload.apps.UploadConfig',
    'apps.documents.apps.DocumentsConfig',
    'apps.carts.apps.CartsConfig',
    'apps.payment.apps.PaymentConfig',
    'apps.comments.apps.CommentsConfig',
    'apps.quiz.apps.QuizConfig',
    'apps.rating.apps.RatingConfig',
    'apps.settings.apps.SettingsConfig',
    'apps.classes.apps.ClassesConfig',
    'apps.posts.apps.PostsConfig',
    'apps.configuration.apps.ConfigurationConfig',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'debug_toolbar',
    'admin_extra_buttons',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_better_admin_arrayfield',
    'django_extensions',
    'ckeditor',
    'ckeditor_uploader',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ecourse.custom_middleware.TimezoneMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecourse.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

WSGI_APPLICATION = 'ecourse.wsgi.application'

AUTH_USER_MODEL = "users.User"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres://postgres:haibinh232@localhost/ecourses"),
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = "Asia/Ho_Chi_Minh"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

DEFAULT_HIDDEN_FILE_EXT = env.str("DEFAULT_HIDDEN_FILE_EXT", default="py")

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "staticfiles/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

TEMPLATES_ROOT = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_ROOT],
        'APP_DIRS': True,
        'OPTIONS': {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        }
    },
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "device-id",
    "client-id",
    "app-version",
)

ALLOWED_HOSTS = [env("DJANGO_ALLOWED_HOSTS", default="*")]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env.int("ACCESS_TOKEN_LIFETIME_MINUTES", default=360)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=env.int("REFRESH_TOKEN_LIFETIME_MINUTES", default=360)),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

EMAIL_USE_TLS = env("EMAIL_USE_TLS", default="EMAIL_USE_TLS")
EMAIL_HOST = env("EMAIL_HOST", default="EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT", default="EMAIL_PORT")

# CKEDITOR
CKEDITOR_BASEPATH = '/staticfiles/ckeditor/ckeditor/'

CKEDITOR_CONFIGS = {
    'default': {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "FontSize",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                # "Undo",
                # "Redo",
            ],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            # ["Smiley", "SpecialChar"],
            ["Templates", "Source"],
        ],
        "toolbar": "Full",
        "height": 500,
        "width": 835,
        "filebrowserWindowWidth": 940,
        "filebrowserWindowHeight": 725,
    }
}


CKEDITOR_UPLOAD_PATH = ""
