from django.test import TestCase
from django.urls import reverse


class APIEndpointTestCase(TestCase):
    def test_schema_url_returns_200(self):
        """
        /schema/ 엔드포인트가 200 OK 상태 코드를 반환하는지 테스트합니다.
        """
        url = reverse('schema')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)