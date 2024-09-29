# inventory/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Item
import time


class InventoryItemTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )

        # Obtain a token for the test user
        self.token = self.client.post(
            '/api/token/', {'username': 'testuser', 'password': 'testpass'}).data['access']

        # Create an initial item
        self.item = Item.objects.create(
            name="Test Item", description="This is a test item."
        )

    def test_create_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(
            '/api/items/',
            {'name': 'New Item',
                'description': 'This is a new item.'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_items(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(
            f'/api/items/{self.item.id}/',
            {'name': 'Updated Item',
                'description': 'Updated description.'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RegisterViewTests(APITestCase):

    def setUp(self):
        # Using timestamp to ensure uniqueness
        self.timestamp = int(time.time())
        self.username = f"uniqueuser{self.timestamp}"
        self.password = "testpass"
        self.email = f"uniqueuser{self.timestamp}@example.com"

    def test_register_user_with_unique_username(self):
        response = self.client.post('/register', {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_existing_username(self):
        # Register the user first
        self.client.post('/register', {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': 'Test',
            'last_name': 'User'
        })

        # Try to register again with the same username
        response = self.client.post('/register', {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_without_username(self):
        response = self.client.post('/register', {
            'password': self.password,
            'email': self.email,
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):

    def setUp(self):
        # Create a user for testing login
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@example.com"
        )

    def test_login_success(self):
        response = self.client.post('/api/token/', {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_username(self):
        response = self.client.post('/api/token/', {
            'username': 'invaliduser',
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_incorrect_password(self):
        response = self.client.post('/api/token/', {
            'username': self.username,
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_empty_credentials(self):
        response = self.client.post('/api/token/', {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_empty_username(self):
        response = self.client.post('/api/token/', {
            'username': '',
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_empty_password(self):
        response = self.client.post('/api/token/', {
            'username': self.username,
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
