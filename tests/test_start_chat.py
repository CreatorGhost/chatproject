import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token

from chatapp.models import UserSession


class StartChatTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_start_chat(self):
        # Creating two users
        user1 = get_user_model().objects.create_user('testuser1', 'password1')
        user2 = get_user_model().objects.create_user('testuser2', 'password2')
        UserSession.objects.create(user=user2, last_activity=timezone.now())
        # Creating a token for user1
        token, created = Token.objects.get_or_create(user=user1)
        print(get_user_model().objects.all())
        # Starting a chat with user2
        response = self.client.post('/api/chat/start/', {
            'recipient': 'testuser2',
        }, HTTP_AUTHORIZATION=f'Token {token.key}', content_type='application/json')
        print(response.content)
        # Checking the response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content)['status'], 'ok')