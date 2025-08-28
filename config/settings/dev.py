# config/settings/dev.py
# 개발 환경용 설정

DEBUG = True

SECRET_KEY = "django-insecure-development-key"

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "testdb",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
