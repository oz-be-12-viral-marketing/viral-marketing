# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import CustomUser

from .models import Notification

User = get_user_model()


class NotificationReadAPITest(APITestCase):

    def setUp(self):
        # 유저 생성
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password123", name="Test User", nickname="testuser"
        )
        self.user.is_active = True
        self.user.save()

        self.other_user = CustomUser.objects.create_user(
            email="other@example.com", password="password123", name="Other User", nickname="otheruser"
        )

        # 인증 처리 (JWT 토큰 필요 없음)
        self.client.force_authenticate(user=self.user)

        # 알림 생성
        self.notification = Notification.objects.create(user=self.user, message="테스트 알림")
        self.other_notification = Notification.objects.create(user=self.other_user, message="다른 유저 알림")

    def test_read_notification_success(self):
        """
        본인 알림을 읽음 처리하는 경우 성공해야 한다.
        """
        url = reverse("notification-read", args=[self.notification.id])
        response = self.client.patch(url)

        self.notification.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.notification.is_read)

    def test_read_other_users_notification_fail(self):
        """
        다른 유저의 알림은 접근 불가해야 한다.
        """
        url = reverse("notification-read", args=[self.other_notification.id])
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_notification_without_login(self):
        """
        로그인하지 않은 유저는 읽기 요청 불가
        """
        self.client.logout()
        url = reverse("notification-read", args=[self.notification.id])
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
