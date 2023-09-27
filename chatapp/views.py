import json
from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .models import Message, UserSession


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        try:
            User.objects.get(username=username)
            return JsonResponse({'error': 'Username already taken'}, status=400)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'status': 'ok', 'token': token.key}, status=201)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.strip())
        print(request.body)
        username = data.get('username')
        password = data.get('password')
        # pdb.set_trace()
        user = authenticate(username=username, password=password)
        if user is not None:
            UserSession.objects.update_or_create(user=user, defaults={'last_activity': datetime.now()})
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key}, status=200)
        else:
            return JsonResponse({'error': 'Invalid login'}, status=400)

import pdb


@csrf_exempt
def start_chat(request):
    if request.method == 'POST':
        
        auth = TokenAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, request.auth = user_auth_tuple
            else:
                raise AuthenticationFailed('Invalid token')
        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)

        data = json.loads(request.body)
        recipient_username = data.get('recipient')
        try:
            recipient = User.objects.get(username=recipient_username)
            # pdb.set_trace() 
            if UserSession.objects.get(user=recipient).last_activity < timezone.now() - timedelta(minutes=5):
                return JsonResponse({'error': 'Recipient is offline'}, status=400)
            return JsonResponse({'status': 'ok'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Recipient does not exist'}, status=400)

        sender = request.user

@csrf_exempt
def send_message(request, room_name):
    if request.method == 'POST':
        auth = TokenAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, request.auth = user_auth_tuple
            else:
                raise AuthenticationFailed('Invalid token')
        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)

        data = json.loads(request.body)
        message = data.get('message')
        sender = request.user.username
        try:
            recipient = User.objects.get(username=room_name)
            if UserSession.objects.get(user=recipient).last_activity < timezone.now() - timedelta(minutes=5):
                return JsonResponse({'error': 'Recipient is offline'}, status=400)
            # Send message to room group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{room_name}',
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender
                }
            )
            Message.objects.create(sender=request.user, recipient=recipient, message=message)
            return JsonResponse({'status': 'ok'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Recipient does not exist'}, status=400)

def online_users(request):
    auth = TokenAuthentication()
    try:
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is not None:
            request.user, request.auth = user_auth_tuple
        else:
            raise AuthenticationFailed('Invalid token')
    except AuthenticationFailed as e:
        return JsonResponse({'error': str(e)}, status=401)

    active_sessions = UserSession.objects.filter(last_activity__gte=timezone.now() - timedelta(minutes=5))
    online_users = [session.user.username for session in active_sessions]
    return JsonResponse({'online_users': online_users}, status=200)




def recommended_friends(request, user_id):
    # Load the JSON file and find the user
    with open('data/users.json') as f:
        users = json.load(f)['users']
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Calculate the similarity score for each user
    for other_user in users:
        if other_user == user:
            other_user['similarity'] = 0
            continue
        common_interests = set(user['interests']).intersection(other_user['interests'])
        interest_score = sum(min(user['interests'][interest], other_user['interests'][interest]) for interest in common_interests)
        age_difference = abs(user['age'] - other_user['age'])
        
        # Normalize the interest score and age difference
        max_interest_score = 100 * len(common_interests)
        max_age_difference = max(user['age'] for user in users) - min(user['age'] for user in users)
        normalized_interest_score = interest_score / max_interest_score if max_interest_score > 0 else 0
        normalized_age_difference = age_difference / max_age_difference if max_age_difference > 0 else 0

        other_user['similarity'] = round(normalized_interest_score - normalized_age_difference, 3)

    # Sort the users by similarity score and return the top 5
    recommended_users = sorted(users, key=lambda x: -x['similarity'])[:5]
    return JsonResponse({'recommended_friends': recommended_users}, status=200)
