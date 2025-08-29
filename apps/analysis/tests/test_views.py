import pytest
from analysis.models import Analysis
from django.urls import reverse
from rest_framework.test import APIClient

from apps.users.models import CustomUser


@pytest.mark.django_db
class TestAnalysisListAPIView:

    def setup_method(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username="testuser")

    def test_get_all_analysis(self):
        Analysis.objects.create(
            user=self.user, type="weekly", period_start="2025-08-01", period_end="2025-08-07", about="총 지출"
        )
        Analysis.objects.create(
            user=self.user, type="monthly", period_start="2025-08-01", period_end="2025-08-31", about="총 수입"
        )

        url = reverse("analysis-list")
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filter_by_type(self):
        Analysis.objects.create(
            user=self.user, type="weekly", period_start="2025-08-01", period_end="2025-08-07", about="총 지출"
        )
        Analysis.objects.create(
            user=self.user, type="monthly", period_start="2025-08-01", period_end="2025-08-31", about="총 수입"
        )

        url = reverse("analysis-list")
        response = self.client.get(url, {"type": "weekly"})

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["type"] == "weekly"
