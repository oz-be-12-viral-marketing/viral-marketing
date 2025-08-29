from rest_framework import serializers

from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            "id",
            "user",
            "about",
            "type",
            "period_start",
            "period_end",
            "description",
            "result_image",
            "created_at",
            "updated_at",
        ]
