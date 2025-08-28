from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Accounts, Transactions

User = get_user_model()


class AccountsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="password123", username="testuser")

    def test_create_account(self):
        account = Accounts.objects.create(user=self.user, account_number="1234567890", balance=Decimal("1000.00"))
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.account_number, "1234567890")
        self.assertEqual(account.balance, Decimal("1000.00"))

    def test_update_account_balance(self):
        account = Accounts.objects.create(user=self.user, account_number="1234567890", balance=Decimal("1000.00"))
        account.balance += Decimal("500.00")
        account.save()
        self.assertEqual(account.balance, Decimal("1500.00"))

    def test_delete_account(self):
        account = Accounts.objects.create(user=self.user, account_number="1234567890", balance=Decimal("1000.00"))
        account_id = account.id
        account.delete()
        self.assertFalse(Accounts.objects.filter(id=account_id).exists())


class TransactionsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="password123", username="testuser")
        self.account = Accounts.objects.create(user=self.user, account_number="1234567890", balance=Decimal("1000.00"))

    def test_create_transaction(self):
        transaction = Transactions.objects.create(
            account=self.account, transaction_type="deposit", amount=Decimal("200.00"), description="Test deposit"
        )
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.amount, Decimal("200.00"))
        self.assertEqual(transaction.transaction_type, "deposit")

    def test_update_transaction(self):
        transaction = Transactions.objects.create(
            account=self.account,
            transaction_type="deposit",
            amount=Decimal("200.00"),
        )
        transaction.amount = Decimal("300.00")
        transaction.save()
        self.assertEqual(transaction.amount, Decimal("300.00"))

    def test_delete_transaction(self):
        transaction = Transactions.objects.create(
            account=self.account,
            transaction_type="deposit",
            amount=Decimal("200.00"),
        )
        transaction_id = transaction.id
        transaction.delete()
        self.assertFalse(Transactions.objects.filter(id=transaction_id).exists())
