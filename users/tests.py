from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserSignupTestCase(APITestCase):
    def test_signup_success(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'nickname': '테스트',
            'password': 'testpass123!',
            'password_confirm': 'testpass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)

    def test_signup_password_mismatch(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'nickname': '테스트',
            'password': 'testpass123!',
            'password_confirm': 'wrongpass!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
