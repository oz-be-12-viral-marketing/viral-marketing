from django.apps import AppConfig
from config.settings.base import BASE_DIR


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    path = BASE_DIR / "core"
