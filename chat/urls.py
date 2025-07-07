from django.urls import path
from .api.view import (
    CreatePrivateChatView, CreateGroupChatView,
    GetChatRoomMembers, CreateMessage,
    GetMessage
)

urlpatterns = [
    path(
        'private/create/',
        CreatePrivateChatView.as_view(),
        name='create_private_chat'
    ),
    path(
        'group/create/',
        CreateGroupChatView.as_view(),
        name='create_group_chat'
    ),
    path(
        'get_chat_room_members/',
        GetChatRoomMembers.as_view(),
        name='get_chat_room_members',
    ),
    path(
        'send_message/',
        CreateMessage.as_view(),
        name='create_message',
    ),
    path(
        'message/',
        GetMessage.as_view(),
        name='get_message',
    ),
]
