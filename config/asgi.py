import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from todo.middleware import TokenAuthMiddleware   # ایمپورت جدید
import todo.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddleware(            # جایگزین AuthMiddlewareStack
        URLRouter(
            todo.routing.websocket_urlpatterns
        )
    ),
})