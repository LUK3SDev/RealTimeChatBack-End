from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


class UserPublicKey(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='public_key'
    )
    public_key = models.TextField()
    key_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"PublicKey for {self.user.username}"


def get_private_chat_name(chat_room, current_user):
    if chat_room.room_type == 'private':
        other_member = chat_room.members.exclude(user=current_user).first()
        return other_member.user.username if other_member else "Chat privata"
    return chat_room.name
