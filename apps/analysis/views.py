import logging

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from apps.transaction_history.models import TransactionHistory

from .models import SentimentAnalysis, SpendingReport
from .serializers import SpendingReportSerializer
from .tasks import generate_spending_report

# Load the sentiment analysis model and tokenizer once when the module is loaded.
# This is more efficient than loading it on every request.
MODEL_NAME = "kykim/bert-kor-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
sentiment_classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_report_api_view(request, period_type):
    if period_type not in ["weekly", "monthly"]:
        return Response(
            {"error": "Invalid period type. Must be 'weekly' or 'monthly'."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Celery 태스크를 비동기적으로 실행하며, 현재 로그인한 사용자의 ID를 전달합니다.
        generate_spending_report.delay(request.user.id, period_type)
    except Exception as e:
        # Redis 연결 실패 등 Celery 작업 전달 중 발생할 수 있는 예외 처리
        logging.getLogger(__name__).error(f"Celery task dispatch failed for user {request.user.id}: {e}")
        return Response(
            {"error": "리포트 생성 작업을 시작하지 못했습니다. 서버 관리자에게 문의하세요."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {"message": f"{period_type.capitalize()} spending report generation initiated."},
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sentiment_analysis_api_view(request, transaction_id):
    try:
        transaction = TransactionHistory.objects.get(pk=transaction_id, account__user=request.user)
    except TransactionHistory.DoesNotExist:
        return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

    text_content = request.data.get("text_content")
    if not text_content:
        return Response({"error": "Text content is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Perform sentiment analysis using the loaded pipeline
    try:
        analysis_results = sentiment_classifier(text_content)
        result = analysis_results[0]
        model_label = result["label"]
        score = result["score"]

        # Translate the model's label ('LABEL_1' or 'LABEL_0') to Korean
        if model_label == "LABEL_1":
            sentiment = "긍정"
        elif model_label == "LABEL_0":
            sentiment = "부정"
        else:
            sentiment = "중립"  # Fallback for any unexpected labels

    except Exception as e:
        logging.getLogger(__name__).error(f"Sentiment analysis model failed: {e}")
        return Response({"error": "감정 분석 모델 실행 중 오류가 발생했습니다."})

    # Save the analysis result
    SentimentAnalysis.objects.create(
        transaction=transaction,
        text_content=text_content,
        sentiment=sentiment,  # Save the translated Korean label
        score=score,
    )

    return Response(
        {
            "message": "Sentiment analysis completed.",
            "sentiment": sentiment,  # Return the translated Korean label
            "score": score,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def report_list_api_view(request):
    # 현재 로그인한 사용자의 리포트만 필터링하여 반환합니다.
    reports = SpendingReport.objects.filter(user=request.user).order_by("-generated_date", "-created_at")

    # [개선] Serializer를 사용하여 복잡한 데이터 변환 로직을 자동화합니다.
    serializer = SpendingReportSerializer(reports, many=True)

    return Response({"reports": serializer.data}, status=status.HTTP_200_OK)
