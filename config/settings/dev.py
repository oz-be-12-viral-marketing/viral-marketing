# config/settings/dev.py

from .base import *

# 개발 환경용 설정
DEBUG = True

SECRET_KEY = 'django-insecure-development-key'

ALLOWED_HOSTS = ['*']
