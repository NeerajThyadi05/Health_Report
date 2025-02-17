
# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")

    def test_login(self):
        login_success = self.client.login(email="test@example.com", password="testpass123")
        self.assertTrue(login_success)