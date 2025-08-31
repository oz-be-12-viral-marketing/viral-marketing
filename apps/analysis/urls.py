from django.urls import path
from .views import SentimentAnalysisView

urlpatterns = [
    path('transactions/<int:transaction_id>/sentiment/', SentimentAnalysisView.as_view(), name='transaction-sentiment-analysis'),
]
