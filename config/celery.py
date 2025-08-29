import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# ───── 여기서 Beat 스케줄 등록 ─────
app.conf.beat_schedule = {
    "weekly-analysis": {
        "task": "analysis.tasks.weekly_analysis_task",
        "schedule": crontab(hour=0, minute=0, day_of_week="mon"),  # 매주 월요일 00:00
    },
    "monthly-analysis": {
        "task": "analysis.tasks.monthly_analysis_task",
        "schedule": crontab(hour=0, minute=0, day_of_month="1"),  # 매월 1일 00:00
    },
}
