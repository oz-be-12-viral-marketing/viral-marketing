from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=255, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.email or self.username


class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.account_number}"


class Transactions(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    TRANSACTION_TYPES = [
        ("deposit", "Deposit"),
        ("withdraw", "Withdraw"),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.account.account_number} - {self.transaction_type} - {self.amount}"
