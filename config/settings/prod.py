# config/settings/prod.py
from . import base  # noqa: F401, F403, F405

DEBUG = False
ALLOWED_HOSTS = ["your-production-domain.com"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

STATIC_ROOT = base.BASE_DIR / "staticfiles"
STATICFILES_DIRS = []
