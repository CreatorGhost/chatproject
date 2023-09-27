
import json

import requests
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token


class UserRegistrationLoginTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_and_login(self):
        # Register a user
        response = self.client.post('/api/register/', {
            'username': 'testuser',
            'password': 'testpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, 'testuser')
        self.assertTrue('token' in json.loads(response.content))

        # Login the user
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in json.loads(response.content))

# !094UCRYtVrYxGZ8iWpxFnPpYDBf9X2le0dQJ02Hf
#authenticate(username=username, password='094UCRYtVrYxGZ8iWpxFnPpYDBf9X2le0dQJ02Hf')


# Found 2 test(s).
# Creating test database for alias 'default'...
# System check identified no issues (0 silenced).
# user :  testuser
# > /Users/adi/code/django/chatproject/chatapp/views.py(42)login()
# -> print(request.body)
# (Pdb) n
# b'{"username": "testuser", "password": "testpassword"}'
# > /Users/adi/code/django/chatproject/chatapp/views.py(43)login()
# -> username = data.get('username')
# (Pdb) n
# > /Users/adi/code/django/chatproject/chatapp/views.py(44)login()
# -> password = data.get('password')
# (Pdb) n
# > /Users/adi/code/django/chatproject/chatapp/views.py(46)login()
# -> user = authenticate(username=username, password=password)
# (Pdb) n
# > /Users/adi/code/django/chatproject/chatapp/views.py(47)login()
# -> if user is not None:
# (Pdb) n
# > /Users/adi/code/django/chatproject/chatapp/views.py(52)login()
# -> return JsonResponse({'error': 'Invalid login'}, status=400)
# (Pdb) c
# Logging   b'{"error": "Invalid login"}'