from django.urls import path

from .views import AnalysisListAPIView

urlpatterns = [
    path("", AnalysisListAPIView.as_view(), name="analysis-list"),
]
