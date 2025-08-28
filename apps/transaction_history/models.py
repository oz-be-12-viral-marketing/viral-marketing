from django.db import models

from apps.accounts.models import Account
from apps.transaction_history.choices import TRANSACTION_METHOD, TRANSACTION_TYPE


# Create your models here.
class TransactionHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_detail = models.CharField(max_length=255, blank=True, null=True)
    transaction_method = models.CharField(max_length=20, choices=TRANSACTION_METHOD)
