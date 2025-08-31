from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import SentimentAnalysis
from apps.transaction_history.models import TransactionHistory
from transformers import pipeline

# 감정 분석 모델을 앱 로딩 시 한 번만 로드합니다.
sentiment_analyzer = pipeline('sentiment-analysis', model='sangrimlee/bert-base-multilingual-cased-nsmc')


class SentimentAnalysisView(APIView):
    def post(self, request, transaction_id, *args, **kwargs):
        # 1. URL로부터 받은 transaction_id로 거래 내역 객체 조회
        transaction = get_object_or_404(TransactionHistory, pk=transaction_id, account__user=request.user)

        # 2. 이미 분석된 거래인지 확인 (OneToOne 관계이므로 중복 방지)
        if hasattr(transaction, 'sentiment_analysis'):
            return Response({'error': 'This transaction has already been analyzed.'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 요청 데이터에서 리뷰 텍스트 가져오기
        text_content = request.data.get('text_content')
        if not text_content:
            return Response({'error': 'text_content is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 4. 감정 분석 수행
        result = sentiment_analyzer(text_content)[0]
        raw_sentiment = result['label']
        score = result['score']

        # 5. 결과 라벨을 한글로 변환
        if raw_sentiment.upper() == 'POSITIVE' or raw_sentiment == 'LABEL_0':
            sentiment = '긍정'
        elif raw_sentiment.upper() == 'NEGATIVE' or raw_sentiment == 'LABEL_1':
            sentiment = '부정'
        else:
            sentiment = raw_sentiment

        # 6. 분석 결과 저장
        analysis_result = SentimentAnalysis.objects.create(
            transaction=transaction,
            text_content=text_content,
            sentiment=sentiment,
            score=score
        )

        # 7. 결과 반환
        return Response({
            'id': analysis_result.id,
            'transaction_id': transaction.id,
            'text_content': analysis_result.text_content,
            'sentiment': analysis_result.sentiment,
            'score': analysis_result.score,
            'created_at': analysis_result.created_at
        }, status=status.HTTP_201_CREATED)