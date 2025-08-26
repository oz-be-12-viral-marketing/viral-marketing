from .dev import *

# 배포용 설정
DEBUG = False
SECRET_KEY = 'real-production-secret-key'  # 배포용 실제 키

ALLOWED_HOSTS = ['yourdomain.com']  # 실제 도메인

# 데이터베이스 (운영용, 예: PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prod_db',
        'USER': 'prod_user',
        'PASSWORD': 'prod_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 추가적인 배포용 설정 예시
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}