import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token

from chatapp.models import UserSession


class OnlineUsersTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_online_users(self):
        # Create multiple users and UserSessions for them
        users = [get_user_model().objects.create_user(f'testuser{i}', 'password') for i in range(3)]
        for user in users:
            UserSession.objects.create(user=user, last_activity=timezone.now())

        # Create a token for the first user
        token, created = Token.objects.get_or_create(user=users[0])

        response = self.client.get('/api/online-users/', HTTP_AUTHORIZATION=f'Token {token.key}')

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        data = json.loads(response.content)
        self.assertIn('online_users', data)
        self.assertIsInstance(data['online_users'], list)
        print("Online Users",data)
        # Check if all users are in the list of online users
        for i in range(3):
            self.assertIn(f'testuser{i}', data['online_users'])

#