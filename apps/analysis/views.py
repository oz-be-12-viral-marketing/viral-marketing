from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import logging

from apps.analysis.tasks import generate_spending_report # Celery 태스크 임포트
from apps.transaction_history.models import TransactionHistory # Added
from .models import SentimentAnalysis, SpendingReport
from .serializers import SpendingReportSerializer # Serializer 임포트


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_report_api_view(request, period_type):
    if period_type not in ['weekly', 'monthly']:
        return Response({"error": "Invalid period type. Must be 'weekly' or 'monthly'."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Celery 태스크를 비동기적으로 실행하며, 현재 로그인한 사용자의 ID를 전달합니다.
        generate_spending_report.delay(request.user.id, period_type)
    except Exception as e:
        # Redis 연결 실패 등 Celery 작업 전달 중 발생할 수 있는 예외 처리
        logging.getLogger(__name__).error(f"Celery task dispatch failed for user {request.user.id}: {e}")
        return Response({"error": "리포트 생성 작업을 시작하지 못했습니다. 서버 관리자에게 문의하세요."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(
        {"message": f"{period_type.capitalize()} spending report generation initiated."},
        status=status.HTTP_202_ACCEPTED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sentiment_analysis_api_view(request, transaction_id):
    try:
        transaction = TransactionHistory.objects.get(pk=transaction_id, account__user=request.user)
    except TransactionHistory.DoesNotExist:
        return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

    text_content = request.data.get('text_content')
    if not text_content:
        return Response({"error": "Text content is required."}, status=status.HTTP_400_BAD_REQUEST)

    # 여기에 실제 감정 분석 로직을 추가합니다.
    # 현재는 플레이스홀더 응답을 반환합니다.
    # 예: 모델 호출, 외부 API 호출 등

    # 임시 감정 분석 결과
    sentiment = "긍정" if "좋아" in text_content or "만족" in text_content else "부정"
    score = 0.95 if sentiment == "긍정" else 0.15

    # 분석 결과를 저장하는 로직 (SentimentAnalysis 모델이 있다면)
    SentimentAnalysis.objects.create( # 주석 해제
        transaction=transaction,
        text_content=text_content,
        sentiment=sentiment,
        score=score
    )

    return Response({
        "message": "Sentiment analysis completed.",
        "sentiment": sentiment,
        "score": score
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_list_api_view(request):
    # 현재 로그인한 사용자의 리포트만 필터링하여 반환합니다.
    reports = SpendingReport.objects.filter(user=request.user).order_by('-generated_date', '-created_at')

    # [개선] Serializer를 사용하여 복잡한 데이터 변환 로직을 자동화합니다.
    serializer = SpendingReportSerializer(reports, many=True)

    return Response({"reports": serializer.data}, status=status.HTTP_200_OK)