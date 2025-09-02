# config/settings/base.py

import os
from datetime import timedelta
from celery.schedules import crontab
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key-for-dev")

# SECURITY WARNING: don't run with debug turned on in production!
# It's a best practice to control DEBUG mode via an environment variable.
# The default is 'True' for easy local development.
# In production, set DJANGO_DEBUG=False as an environment variable.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROOT_URLCONF = "config.urls"

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
]

CUSTOM_APPS = [
    "core",
    "apps.accounts",
    "apps.transaction_history",
    "apps.users",
    "apps.notifications",
    "apps.analysis",
    "apps.frontend",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.naver",
    "allauth.socialaccount.providers.kakao",
    "django_celery_beat",
    "debug_toolbar", # Unconditionally included
]

# Application definition

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

# allauth settings
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGIN_METHODS = ["email"]  # Use the modern, explicit setting
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False  # Explicitly set to False
ACCOUNT_EMAIL_VERIFICATION = "none"
# Since we use a CustomSignupForm, allauth does not need to manage any signup fields itself.
# The CustomSignupForm handles the fields for local registration.
ACCOUNT_SIGNUP_FIELDS = []  # This prevents the critical error
ACCOUNT_FORMS = {
    "signup": "apps.users.forms.CustomSignupForm",
}
ACCOUNT_SIGNUP_REDIRECT_URL = "/accounts/signup/complete/"
ACCOUNT_AUTHENTICATE_ON_REGISTRATION = True


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "naver": {},
    "kakao": {},
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
    "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (user uploaded content)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

# DRF Spectacular settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "apps.users.authentication.JWTCookieAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# Celery Settings
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0' 
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul' # 한국 시간대로 설정
CELERY_TASK_TRACK_STARTED = True # Task가 시작되었을 때 상태를 STARTED로 변경
CELERY_TASK_TIME_LIMIT = 30 * 60 # 30분 이상 걸리는 Task는 강제 종료
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True # Celery worker 시작 시 브로커 연결 재시도

CELERY_BEAT_SCHEDULE = {
    'generate-weekly-spending-report': {
        'task': 'apps.analysis.tasks.schedule_all_user_reports',
        'schedule': crontab(day_of_week='monday', hour=0, minute=0),  # 매주 월요일 00:00에 실행
        'args': ('weekly',),
        'options': {'expires': 300},
    },
    'generate-monthly-spending-report': {
        'task': 'apps.analysis.tasks.schedule_all_user_reports',
        'schedule': crontab(day_of_month='1', hour=0, minute=0),  # 매월 1일 00:00에 실행
        'args': ('monthly',),
        'options': {'expires': 300},
    },
}
