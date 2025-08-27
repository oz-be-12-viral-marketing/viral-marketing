from django.db import models

from apps.accounts.choices import ACCOUNT_TYPE, BANK_CODES, CURRENCIES
from apps.users.models import User


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    bank_code = models.CharField(max_length=3, choices=BANK_CODES)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="KRW")
