from django.db import models

from apps.accounts.models import Account
from apps.transaction_history.choices import TransactionMethod, TransactionType, TransactionCategory


# Create your models here.
class TransactionHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    category = models.CharField(max_length=20, choices=TransactionCategory.choices, default=TransactionCategory.OTHER)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_detail = models.CharField(max_length=255, blank=True, null=True)
    transaction_method = models.CharField(max_length=20, choices=TransactionMethod.choices)
    created_at = models.DateTimeField(auto_now_add=True)