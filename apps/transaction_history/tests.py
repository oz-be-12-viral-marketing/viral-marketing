from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Account
from apps.transaction_history.models import TransactionHistory
from apps.users.models import CustomUser


class TransactionHistoryViewSetTestCase(APITestCase):
    def setUp(self):
        """테스트 케이스를 위한 초기 설정"""
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
            name="Test User",
            nickname="testuser",
            phone_number="01012345678",
        )
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.account = Account.objects.create(
            user=self.user,
            account_number="110-220-330440",
            bank_code="088",  # 신한은행
            account_type="checking",
            balance=Decimal("100000.00"),
            currency="KRW",
        )

        self.transaction = TransactionHistory.objects.create(
            account=self.account,
            transaction_type="DEPOSIT",
            amount=Decimal("50000.00"),
            balance_after=self.account.balance + Decimal("50000.00"),
            transaction_detail="Test Deposit",
            transaction_method="ATM",
        )
        self.account.balance += Decimal("50000.00")
        self.account.save()

        self.url = reverse("transaction-list")

    def test_list_transactions(self):
        """거래 내역 목록 조회 테스트"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.transaction.id)

    def test_retrieve_transaction(self):
        """특정 거래 내역 상세 조회 테스트"""
        url = reverse("transaction-detail", kwargs={"pk": self.transaction.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["amount"], f"{self.transaction.amount:.2f}"
        )  # DecimalField는 문자열로 반환될 수 있음

    def test_create_deposit_transaction(self):
        """입금 거래 생성 테스트"""
        initial_balance = self.account.balance
        deposit_amount = Decimal("30000.00")
        data = {
            "account": self.account.pk,
            "transaction_type": "DEPOSIT",
            "amount": deposit_amount,
            "transaction_detail": "Salary",
            "transaction_method": "TRANSFER",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.account.refresh_from_db()
        expected_balance = initial_balance + deposit_amount
        self.assertEqual(self.account.balance, expected_balance)
        self.assertEqual(response.data["balance_after"], f"{expected_balance:.2f}")
        self.assertTrue(TransactionHistory.objects.filter(pk=response.data["id"]).exists())

    def test_create_withdrawal_transaction(self):
        """출금 거래 생성 테스트"""
        initial_balance = self.account.balance
        withdrawal_amount = Decimal("20000.00")
        data = {
            "account": self.account.pk,
            "transaction_type": "WITHDRAW",
            "amount": withdrawal_amount,
            "transaction_detail": "Groceries",
            "transaction_method": "CARD",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.account.refresh_from_db()
        expected_balance = initial_balance - withdrawal_amount
        self.assertEqual(self.account.balance, expected_balance)
        self.assertEqual(response.data["balance_after"], f"{expected_balance:.2f}")

    def test_create_withdrawal_insufficient_funds(self):
        """잔액 부족 출금 시도 테스트"""
        initial_balance = self.account.balance
        withdrawal_amount = initial_balance + Decimal("100.00")
        data = {
            "account": self.account.pk,
            "transaction_type": "WITHDRAW",
            "amount": withdrawal_amount,
            "transaction_detail": "Too much shopping",
            "transaction_method": "CARD",
        }
        response = self.client.post(self.url, data, format="json")
        # The view raises a generic serializers.ValidationError, which typically results in a 400 Bad Request.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, initial_balance)  # 잔액은 변하지 않아야 함

    def test_delete_transaction(self):
        """거래 내역 삭제 테스트"""
        # 일반적으로 거래 내역은 삭제하지 않지만, ViewSet이 허용하므로 테스트합니다.
        url = reverse("transaction-detail", kwargs={"pk": self.transaction.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TransactionHistory.objects.filter(pk=self.transaction.pk).exists())
