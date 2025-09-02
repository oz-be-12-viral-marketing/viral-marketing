from django.conf import settings
from django.db import models

from apps.transaction_history.models import TransactionHistory  # Added


class SpendingReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="spending_reports",
        help_text="The user this report belongs to.",
    )
    REPORT_TYPE_CHOICES = [
        ("weekly", "주간 리포트"),
        ("monthly", "월간 리포트"),
    ]
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    generated_date = models.DateField()
    json_data = models.JSONField(default=dict, help_text="Report data in JSON format.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-user", "-generated_date", "-created_at"]
        # A user should only have one report of a specific type for a specific day.
        unique_together = ("user", "report_type", "generated_date")

    def __str__(self):
        return f"{self.get_report_type_display()} for {self.user} - {self.generated_date}"


class SentimentAnalysis(models.Model):
    transaction = models.ForeignKey(TransactionHistory, on_delete=models.CASCADE)
    text_content = models.TextField()
    sentiment = models.CharField(max_length=50)  # 예: POSITIVE, NEGATIVE, NEUTRAL
    score = models.FloatField()  # 감정 점수
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Analysis for {self.transaction.transaction_detail}: {self.sentiment} ({self.score})"
