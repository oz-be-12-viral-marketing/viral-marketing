from rest_framework import generics

from .models import Analysis
from .serializers import AnalysisSerializer


class AnalysisListAPIView(generics.ListAPIView):
    serializer_class = AnalysisSerializer

    def get_queryset(self):
        queryset = Analysis.objects.all()
        period_type = self.request.query_params.get("type")  # ?type=weekly 또는 monthly

        if period_type in ["weekly", "monthly"]:
            queryset = queryset.filter(type=period_type)
        return queryset
