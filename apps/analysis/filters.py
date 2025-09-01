import django_filters
from django import forms
from .models import SentimentAnalysis

SENTIMENT_CHOICES = (
    ('긍정', '긍정'),
    ('부정', '부정'),
)


class AnalysisFilter(django_filters.FilterSet):
    text_content = django_filters.CharFilter(
        lookup_expr='icontains',
        label='리뷰 내용',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '내용, 메모 등'})
    )
    sentiment = django_filters.ChoiceFilter(
        label='감정',
        choices=SENTIMENT_CHOICES,
        empty_label="모든 감정",
        widget=forms.Select(attrs={'class': 'form-select form-control'})
    )
    start_date = django_filters.DateFilter(
        field_name='transaction__created_at',
        lookup_expr='gte',
        label='시작일',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = django_filters.DateFilter(
        field_name='transaction__created_at',
        lookup_expr='lte',
        label='종료일',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = SentimentAnalysis
        fields = ['text_content', 'sentiment', 'start_date', 'end_date']