# chat_backend/chat_backend/routing.py
from django.urls import re_path

# Per ora, mettiamo un consumer di esempio.
# Dovremo creare questo consumer in una delle nostre app Django.
from chat import consumers  # Questo è solo un placeholder per ora

websocket_urlpatterns = [
    re_path(
        r'ws/chat/(?P<room_name>[^/]+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
]
