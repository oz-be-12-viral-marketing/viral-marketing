import pytest
from django.utils import timezone

from apps.analysis.analyzers import Analyzer
from apps.transaction_history.models import Transaction
from apps.users.models import CustomUser


@pytest.mark.django_db
def test_analyzer_creates_analysis():
    user = CustomUser.objects.create(username="testuser")
    Transaction.objects.create(user=user, date=timezone.now().date(), amount=1000, category="food")

    analyzer = Analyzer(user=user, start_date="2025-08-01", end_date="2025-08-31")
    result = analyzer.run()

    assert result.about == "총 지출"
    assert result.result_image
