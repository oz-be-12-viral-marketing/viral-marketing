from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TransactionHistory


@receiver(post_save, sender=TransactionHistory)
def notify_transaction(sender, instance, created, **kwargs):
    if created:
        print(f"새 거래 기록 생성: {instance.transaction_type} {instance.amount}")
