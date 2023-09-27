
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        from rest_framework.authtoken.models import Token 
        headers = dict(scope['headers'])
        if b'cookie' in headers:
            cookies = headers[b'cookie'].decode()
            print(f"Cookies: {cookies.split('=')}") 
            token_name, token_key = cookies.split('=')[0],cookies.split('=')[-1]
            if token_name == 'Token':
                try:
                    scope['user'] =  await sync_to_async(self.get_user_from_token)(token_key)
                except Token.DoesNotExist:
                    scope['user'] = AnonymousUser()
        return await self.inner(scope, receive, send)  
    def get_user_from_token(self, token_key):
        from rest_framework.authtoken.models import Token 
        token = Token.objects.get(key=token_key)
        return token.user
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))