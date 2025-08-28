from . import base

# 개발 환경용 설정
DEBUG = True

SECRET_KEY = "django-insecure-development-key"

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "testdb",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432",
    }
}

# Copy all settings from base.py
for setting in dir(base):
    if setting.isupper():  # Only copy uppercase settings
        globals()[setting] = getattr(base, setting)