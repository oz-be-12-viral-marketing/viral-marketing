from django.urls import path
from .views import SentimentAnalysisView

urlpatterns = [
    path('sentiment/', SentimentAnalysisView.as_view(), name='sentiment-analysis'),
]
