from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from authentication.models import User


class RegisterViewTest(APITestCase):

    def test_register_success(self):
        url = reverse('authentication:register')
        data = {'email': 'test@example.com', 'phone': '1234567890', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_existing_user(self):
        # Create a user with same email and phone
        User.objects.create(email='test@example.com', phone='1234567890', password='password')
        url = reverse('authentication:register')
        data = {'email': 'test@example.com', 'phone': '1234567890', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmailVerifyViewTest(APITestCase):

    def test_email_verify_success(self):
        # Assuming valid token and email
        url = reverse('authentication:register_verify')
        data = {'token': 'valid_token', 'email': 'test@example.com'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_verify_invalid_token(self):
        # Assuming invalid token
        url = reverse('authentication:register_verify')
        data = {'token': 'invalid_token', 'email': 'test@example.com'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_verify_user_not_found(self):
        # Assuming user not found for given token
        url = reverse('authentication:register_verify')
        data = {'token': 'valid_token', 'email': 'test@example.com'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FacebookLoginTest(APITestCase):

    @patch('social_django.utils.psycopg2')
    def test_facebook_login_success(self, mock_psa):
        url = reverse('authentication:facebook_login')
        data = {'access_token': 'valid_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_facebook_login_invalid_token(self):
        url = reverse('authentication:facebook_login')
        data = {'access_token': 'invalid_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GoogleLoginTest(APITestCase):
    
    @patch('social_django.utils.psycopg2')
    def test_google_login_success(self, mock_psa):
        url = reverse('authentication:google_login')
        data = {'access_token': 'valid_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_google_login_invalid_token(self):
        url = reverse('authentication:google_login')
        data = {'access_token': 'invalid_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
