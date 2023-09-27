
import json

import requests
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token


class RecommendedFriendsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_recommended_friends(self):
        user_id = 1

        response = self.client.get(f'/api/suggested-friends/{user_id}/')

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        data = json.loads(response.content)
        self.assertIn('recommended_friends', data)
        self.assertIsInstance(data['recommended_friends'], list)
        self.assertLessEqual(len(data['recommended_friends']), 5)