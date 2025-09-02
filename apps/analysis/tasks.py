import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict

from celery import shared_task
from django.db.models import Case, CharField, F, Sum, Value, When
from django.utils import timezone

from apps.transaction_history.choices import TransactionCategory  # New import
from apps.transaction_history.models import TransactionHistory
from apps.users.models import CustomUser

from .models import SpendingReport

logger = logging.getLogger(__name__)


def _get_date_range_for_period(period_type: str, now: datetime) -> tuple[datetime, datetime]:
    """
    주어진 기간 유형('weekly' 또는 'monthly')에 따라 시작일과 종료일(datetime)을 계산합니다.
    """
    if period_type == "weekly":
        start_of_week = now - timedelta(days=now.weekday())
        start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6)
        end_date = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start_date, end_date
    elif period_type == "monthly":
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (start_of_month + timedelta(days=32)).replace(day=1)
        end_date = next_month - timedelta(microseconds=1)
        return start_of_month, end_date
    else:
        raise ValueError(f"Invalid period_type: {period_type}")


@shared_task
def schedule_all_user_reports(period_type: str):
    """
    모든 활성 사용자를 대상으로 리포트 생성을 스케줄링하는 마스터 태스크입니다.
    """
    user_ids = CustomUser.objects.filter(is_active=True).values_list("id", flat=True)
    logger.info(f"Starting {period_type} report generation for {len(user_ids)} users.")
    for user_id in user_ids:
        generate_spending_report.delay(user_id, period_type)


@shared_task
def generate_spending_report(user_id: int, period_type: str) -> str:
    """
    지정된 사용자와 기간(주간/월간)에 대한 소비 리포트를 생성합니다.

    이 태스크는 데이터베이스에서 직접 집계를 수행하여 효율적으로 처리합니다.
    """
    now: datetime = timezone.now()
    today: date = now.date()

    try:
        # [개선] 날짜 계산 로직을 헬퍼 함수로 분리하여 가독성 및 재사용성 향상
        start_date, end_date = _get_date_range_for_period(period_type, now)
    except ValueError as e:
        logger.warning("리포트 생성 실패 (user: %s): %s", user_id, e)
        return f"리포트 생성 실패: 유효하지 않은 기간 유형 '{period_type}'."

    # TransactionHistory는 account를 통해 User에 연결되므로, account__user_id로 필터링합니다.
    transactions = TransactionHistory.objects.filter(
        account__user_id=user_id,
        created_at__range=(start_date, end_date),
    ).order_by("created_at")

    if transactions.exists():
        # 입금 내역은 '수입' 카테고리로 분류하고, 출금 내역은 기존 카테고리를 사용합니다.
        # Django ORM의 조건부 표현식을 사용하여 report_category를 정의합니다.
        categorized_transactions = transactions.annotate(
            report_category=Case(
                When(transaction_type="DEPOSIT", then=Value(TransactionCategory.INCOME)),
                default=F("category"),
                output_field=CharField(),
            )
        )

        # 카테고리별 지출 합계를 계산합니다.
        category_spending = (
            categorized_transactions.values("report_category")  # 새로운 report_category로 그룹화
            .annotate(total_spending=Sum("amount"))  # 각 카테고리의 지출 합계 계산
            .order_by("report_category")
        )
        # 데이터를 JSON 직렬화 가능한 형식으로 변환
        report_data: Dict[str, Any] = {
            "categories": [TransactionCategory(item["report_category"]).label for item in category_spending],
            "spending": [float(item["total_spending"]) for item in category_spending],
        }
        final_message = f"Successfully generated {period_type} report for user {user_id}."
    else:
        # 데이터가 없는 경우, 프론트엔드가 일관되게 처리할 수 있도록 빈 데이터 구조를 설정합니다.
        report_data = {"categories": [], "spending": []}
        final_message = f"No data for {period_type} report for user {user_id}."

    try:
        # [개선] 데이터 유무에 관계없이, 결정된 report_data를 사용하여 DB에 한 번만 접근합니다.
        _report, created = SpendingReport.objects.update_or_create(
            user_id=user_id, report_type=period_type, generated_date=today, defaults={"json_data": report_data}
        )

        action = "생성" if created else "업데이트"
        logger.info("%s 리포트가 성공적으로 %s되었습니다 (user: %s).", period_type.capitalize(), action, user_id)
    except Exception as e:
        logger.error("SpendingReport 저장 중 오류 발생 (user: %s, type: %s): %s", user_id, period_type, e)
        raise  # 오류를 다시 발생시켜 Celery가 실패를 기록하도록 함

    return final_message
