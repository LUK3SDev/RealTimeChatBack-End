from django.db import models
from account.models import User
import uuid


class ChatRoom(models.Model):
    PRIVATE = 'private'
    GROUP = 'group'
    ROOM_TYPE_CHOICES = [
        (PRIVATE, 'Private'),
        (GROUP, 'Group'),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or str(self.id)


class ChatRoomMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='members'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'user',
            'chat_room',
        )

    def __str__(self):
        return f"{self.user} in {self.chat_room}"


class Message(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages',
        default=None, null=True, blank=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key_id = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        # mostra solo i primi 20 caratteri
        return f"{self.sender}: {self.content[:20]}..."
