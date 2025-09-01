from django import forms
from .models import SentimentAnalysis # 주석 해제

SENTIMENT_CHOICES = (
    ('긍정', '긍정'),
    ('부정', '부정'),
)


class SentimentAnalysisEditForm(forms.ModelForm): # 주석 해제
    sentiment = forms.ChoiceField(
        choices=SENTIMENT_CHOICES,
        widget=forms.RadioSelect,
        label='감정'
    )

    class Meta:
        model = SentimentAnalysis
        fields = ['text_content', 'sentiment']
        widgets = {
            'text_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'text_content': '리뷰 내용',
        }
