import os

# 기본값: 개발 환경
ENVIRONMENT = os.getenv("DJANGO_ENV", "dev").lower()

if ENVIRONMENT == "prod":
    pass
else:
    pass
