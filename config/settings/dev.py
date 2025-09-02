# config/settings/dev.py
# 개발 환경용 설정
import os
from .base import *  # noqa: F403

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-development-key") # Load from env var

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "testdb"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Debug Toolbar settings for development
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0"] # Broad IP range for development
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True, # Force show for debugging
    "IS_RUNNING_TESTS": False, # Disable check during tests
}

# Add Debug Toolbar middleware directly in dev.py
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']