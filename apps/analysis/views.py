from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SentimentAnalysis
from django.contrib.auth import get_user_model
from transformers import pipeline

User = get_user_model()

# 감정 분석 모델을 앱 로딩 시 한 번만 로드합니다.
sentiment_analyzer = pipeline('sentiment-analysis', model='sangrimlee/bert-base-multilingual-cased-nsmc')


class SentimentAnalysisView(APIView):
    def post(self, request, *args, **kwargs):
        text_content = request.data.get('text_content')

        if not text_content:
            return Response({'error': 'text_content is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 미리 로드된 분석기 사용
        result = sentiment_analyzer(text_content)[0]
        raw_sentiment = result['label']
        score = result['score']

        # 결과를 한글로 변환 (개선)
        if raw_sentiment.upper() == 'POSITIVE' or raw_sentiment == 'LABEL_0':
            sentiment = '긍정'
        elif raw_sentiment.upper() == 'NEGATIVE' or raw_sentiment == 'LABEL_1':
            sentiment = '부정'
        else:
            sentiment = raw_sentiment  # 예외적인 경우(e.g. 중립)를 위해 원래 값 사용
        
        # 임시로 첫 번째 사용자를 가져와서 사용
        # 실제 프로덕션에서는 인증된 사용자를 사용해야 합니다.
        user = User.objects.first()
        if not user:
            return Response({'error': 'No user found in the database.'}, status=status.HTTP_400_BAD_REQUEST)


        analysis_result = SentimentAnalysis.objects.create(
            user=user,
            text_content=text_content,
            sentiment=sentiment,
            score=score
        )

        return Response({
            'id': analysis_result.id,
            'text_content': analysis_result.text_content,
            'sentiment': analysis_result.sentiment,
            'score': analysis_result.score,
            'created_at': analysis_result.created_at
        }, status=status.HTTP_201_CREATED)
