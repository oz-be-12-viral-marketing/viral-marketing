from datetime import date, timedelta

from celery import shared_task

from apps.users.models import CustomUser

from .analyzers import Analyzer


@shared_task
def weekly_analysis_task():
    today = date.today()
    start = today - timedelta(days=7)
    for user in CustomUser.objects.all():
        analyzer = Analyzer(user=user, start_date=start, end_date=today, analysis_type="weekly")
        analyzer.run()


@shared_task
def monthly_analysis_task():
    today = date.today()
    start = today.replace(day=1)
    for user in CustomUser.objects.all():
        analyzer = Analyzer(user=user, start_date=start, end_date=today, analysis_type="monthly")
        analyzer.run()
