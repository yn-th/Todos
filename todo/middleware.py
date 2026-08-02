# todo/middleware.py
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.apps import apps
from django.conf import settings

@database_sync_to_async
def get_user_from_token(token):
    # ایمپورت‌های با تأخیر
    from rest_framework_simplejwt.tokens import AccessToken
    User = apps.get_model(settings.AUTH_USER_MODEL)
    try:
        access_token = AccessToken(token)
        return User.objects.get(id=access_token['user_id'])
    except Exception:
        return None   # در صورت نامعتبر بودن توکن

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token', [None])[0]
        scope['user'] = await get_user_from_token(token) if token else None
        return await self.inner(scope, receive, send)