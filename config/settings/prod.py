# config/settings/prod.py
from .base import *  # noqa: F403, F405

DEBUG = False

ALLOWED_HOSTS = ["your-production-domain.com"]

ROOT_URLCONF = "config.urls"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HTTPS Enforcement
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
STATICFILES_DIRS = []
