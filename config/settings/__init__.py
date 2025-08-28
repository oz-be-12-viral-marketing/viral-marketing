import os

# 기본값: 개발 환경
ENVIRONMENT = os.getenv("DJANGO_ENV", "dev").lower()

if ENVIRONMENT == "prod":
    from . import prod as current_settings
else:
    from . import dev as current_settings

# Copy all settings from the selected environment
for setting in dir(current_settings):
    if setting.isupper():  # Only copy uppercase settings
        globals()[setting] = getattr(current_settings, setting)