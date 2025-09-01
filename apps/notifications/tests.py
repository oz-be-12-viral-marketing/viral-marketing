# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Notification

User = get_user_model()


class NotificationReadAPITest(APITestCase):

    def setUp(self):
        # 테스트용 유저 생성
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass", nickname="testuser_nick")
        self.other_user = User.objects.create_user(email="otheruser@example.com", password="testpass", nickname="otheruser_nick")

        # 로그인 처리 및 JWT 토큰 획득
        login_data = {"email": "testuser@example.com", "password": "testpass"}
        login_url = reverse("login")
        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]

        # JWT 토큰을 쿠키에 설정
        self.client.cookies["access_token"] = self.access_token
        self.client.cookies["refresh_token"] = self.refresh_token

        # 알림 생성
        self.notification = Notification.objects.create(user=self.user, message="Test notification", is_read=False)
        self.other_notification = Notification.objects.create(
            user=self.other_user, message="Other user's notification", is_read=False
        )

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
