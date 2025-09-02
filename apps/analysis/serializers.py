from rest_framework import serializers

from .models import SpendingReport


class SpendingReportSerializer(serializers.ModelSerializer):
    """
    SpendingReport 모델을 위한 Serializer.
    API 응답 형식을 정의하고 데이터 유효성 검사를 자동화합니다.
    """

    # 모델에 정의된 get_report_type_display() 메서드의 결과를 포함시킵니다.
    report_type_display = serializers.CharField(source="get_report_type_display", read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = SpendingReport
        fields = ["id", "report_type", "report_type_display", "generated_date", "name", "json_data", "created_at"]

    def get_name(self, obj):
        """프론트엔드에서 필요한 'name' 필드를 동적으로 생성합니다."""
        return f"{obj.get_report_type_display()} - {obj.generated_date.strftime('%Y-%m-%d')}"
