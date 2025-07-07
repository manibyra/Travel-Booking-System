from django.test import TestCase
from .models.user import CustomUser

class UserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            full_name="Test User",
            phone="9876543210",
            aadhaar_no="123456789012",
            address="123 Test Street"
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))
