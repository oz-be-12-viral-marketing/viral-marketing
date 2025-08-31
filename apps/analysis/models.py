from django.db import models

from apps.analysis.choices import ANALYSIS_PERIOD, ANALYSIS_TYPE
from apps.users.models import CustomUser


# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=ANALYSIS_TYPE)
    period = models.CharField(max_length=10, choices=ANALYSIS_PERIOD)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    rusult_image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SentimentAnalysis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text_content = models.TextField()
    sentiment = models.CharField(max_length=10)  # e.g., Positive, Negative, Neutral
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.sentiment}] {self.text_content[:50]}"