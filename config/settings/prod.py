# config/settings/prod.py
from .base import BASE_DIR  # noqa: F403,F405

DEBUG = False

ALLOWED_HOSTS = ["your-production-domain.com"]

ROOT_URLCONF = "config.urls"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []
