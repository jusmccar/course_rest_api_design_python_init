from django.test import TestCase
from ninja.testing import TestClient
from api.endpoints.bark import router as bark_router


class TestBarking(TestCase):
    def setUp(self):
        self.client = TestClient(router_or_app=bark_router)

    def test_web_home(self):
        response = self.client.get("/bark/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "bark!"})