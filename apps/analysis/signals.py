from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import AnalysisResult


@receiver(post_delete, sender=AnalysisResult)
def cleanup_analysis(sender, instance, **kwargs):
    print(f"AnalysisResult {instance.id} 이 성공적으로 삭제되었습니다.")
