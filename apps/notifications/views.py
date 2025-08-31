# Create your views here.
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class UnreadNotificationListView(ListAPIView):
    """
    요청한 유저의 읽지 않은 알림 리스트 조회 API
    """

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by("-created_at")


class NotificationReadAPIView(UpdateAPIView):
    """
    알림 읽음 처리 API
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인한 유저의 알림만 조회 가능하도록 제한
        return Notification.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # 읽음 여부를 True로 강제 세팅
        serializer.save(is_read=True)
