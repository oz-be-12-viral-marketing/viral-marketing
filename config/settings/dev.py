# config/settings/dev.py
# 개발 환경용 설정
import os

from .base import *  # noqa: F403

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-development-key")  # Load from env var

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "mydb"),
        "USER": os.environ.get("DB_USER", "myuser"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "mypassword"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
