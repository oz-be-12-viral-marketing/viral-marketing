from .base import *

# 개발 환경용 설정
DEBUG = True

SECRET_KEY = "django-insecure-development-key"

ALLOWED_HOSTS = ["*"]

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "testdb",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "db",
#         "PORT": "5432",
#     }
# }