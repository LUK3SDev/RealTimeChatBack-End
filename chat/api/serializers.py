from chat.models import ChatRoom, ChatRoomMember, Message
from rest_framework import serializers
from account.models import User
from account.api.serializers import UserSerializer


class PrivateChatCreateSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        help_text="Email o username del destinatario"
    )

    def validate_identifier(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=value)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "Nessun utente trovato con questa email o username."
                )
        return user


class GroupChatCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(
        allow_blank=True, required=False
    )
    members = serializers.ListField(
        child=serializers.CharField(),
        help_text="Lista di email o username dei membri da aggiungere"
    )

    def validate_members(self, value):
        users = []
        for identifier in value:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=identifier)
                except User.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Utente '{identifier}' non trovato."
                    )
            users.append(user)
        return users


class ChatRoomMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ChatRoomMember
        fields = ['id', 'user', 'chat_room']


class MessageCreateSerializer(serializers.Serializer):
    chat_room_id = serializers.UUIDField()
    content = serializers.CharField(max_length=1000)
    receiver = serializers.CharField(required=False, allow_blank=True)
    key_id = serializers.CharField(required=False, allow_blank=True)

    def validate_chat_room_id(self, value):
        try:
            chat_room = ChatRoom.objects.get(id=value)
            return chat_room
        except ChatRoom.DoesNotExist:
            raise serializers.ValidationError("Chat room non trovata.")

    def validate_receiver(self, value):
        if not value:
            return None
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=value)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "Destinatario non trovato."
                )
        return user


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'description', 'room_type', 'created_at']




class GetMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'receiver', 'content', 'created_at', 'key_id']

