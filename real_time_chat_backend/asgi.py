# chat_backend/chat_backend/asgi.py

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set Django settings before importing routing
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 
    'real_time_chat_backend.settings'
)
django.setup()

# Import routing after Django is set up
import real_time_chat_backend.routing  # noqa: E402

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Aggiungi questa parte per la gestione dei WebSockets
    "websocket": AuthMiddlewareStack(
        URLRouter(
            real_time_chat_backend.routing.websocket_urlpatterns
        )
    ),
})