import django_filters
from django import forms
from .models import TransactionHistory
from .choices import TRANSACTION_TYPE


class TransactionFilter(django_filters.FilterSet):
    transaction_detail = django_filters.CharFilter(
        lookup_expr='icontains',
        label='거래 내용',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '내용, 메모 등'})
    )
    transaction_type = django_filters.ChoiceFilter(
        label='거래 유형',
        choices=TRANSACTION_TYPE,
        empty_label="모든 유형",
        widget=forms.Select(attrs={'class': 'form-select form-control'})
    )
    start_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='시작일',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='종료일',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = TransactionHistory
        fields = []