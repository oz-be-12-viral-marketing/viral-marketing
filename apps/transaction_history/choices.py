from django.db import models


class TransactionType(models.TextChoices):
    DEPOSIT = "DEPOSIT", "입금"
    WITHDRAW = "WITHDRAW", "출금"


class TransactionMethod(models.TextChoices):
    TRANSFER = "TRANSFER", "계좌이체"
    CARD = "CARD", "카드"
    CASH = "CASH", "현금"
    ETC = "ETC", "기타"


class TransactionCategory(models.TextChoices):
    FOOD = "FOOD", "식비"
    TRANSPORTATION = "TRANSPORTATION", "교통"
    SHOPPING = "SHOPPING", "쇼핑"
    HOUSING = "HOUSING", "주거"
    UTILITIES = "UTILITIES", "공과금"
    ENTERTAINMENT = "ENTERTAINMENT", "문화/여가"
    HEALTH = "HEALTH", "건강/의료"
    EDUCATION = "EDUCATION", "교육"
    FINANCE = "FINANCE", "금융"
    OTHER = "OTHER", "기타"
    INCOME = "INCOME", "수입"  # Added for reporting
