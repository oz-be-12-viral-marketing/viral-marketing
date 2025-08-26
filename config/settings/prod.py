# config/settings/prod.py

from .base import *

# 배포 환경용 설정
DEBUG = False

# 실제 운영에서는 환경 변수에서 SECRET_KEY를 가져오므로, base.py의 설정이 사용됩니다.
# SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['your-production-domain.com'] # 실제 서비스 도메인을 입력하세요.

# 추가적인 배포용 설정 예시
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
