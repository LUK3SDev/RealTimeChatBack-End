from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from chat.models import ChatRoom, ChatRoomMember, Message
from .serializers import (
    ChatRoomMemberSerializer,
    GetMessageSerializer, 
    PrivateChatCreateSerializer, 
    GroupChatCreateSerializer,
    MessageCreateSerializer
)


class CreatePrivateChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PrivateChatCreateSerializer(data=request.data)
        if serializer.is_valid():
            user1 = request.user
            user2 = serializer.validated_data['identifier']
            # Ordina gli id per evitare duplicati
            users = sorted([user1, user2], key=lambda u: u.id)
            # Cerca se esiste già una chat privata tra questi due utenti
            existing = ChatRoom.objects.filter(
                room_type=ChatRoom.PRIVATE,
                members__user=users[0]
            ).filter(
                members__user=users[1]
            ).distinct().first()
            if existing:
                return Response(
                    {'chat_room_id': str(existing.id)},
                    status=status.HTTP_200_OK
                )
            # Crea la chat privata
            chat_room = ChatRoom.objects.create(room_type=ChatRoom.PRIVATE)
            ChatRoomMember.objects.create(user=users[0], chat_room=chat_room)
            ChatRoomMember.objects.create(user=users[1], chat_room=chat_room)
            return Response(
                {'chat_room_id': str(chat_room.id)},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGroupChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = GroupChatCreateSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            description = serializer.validated_data.get('description', '')
            users = serializer.validated_data['members']
            # Crea la chat di gruppo
            chat_room = ChatRoom.objects.create(
                name=name,
                description=description,
                room_type=ChatRoom.GROUP
            )
            # Aggiungi il creatore e i membri
            ChatRoomMember.objects.create(
                user=request.user, chat_room=chat_room
            )
            for user in users:
                if user != request.user:
                    ChatRoomMember.objects.create(
                        user=user, chat_room=chat_room
                    )
            return Response(
                {'chat_room_id': str(chat_room.id)},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetChatRoomMembers(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        chat_room_id = request.query_params.get('chat_room_id')
        print(chat_room_id)
        chatRoom = ChatRoom.objects.get(id=chat_room_id)
        chatRoomMember = ChatRoomMember.objects.filter(chat_room=chatRoom)
        serializer = ChatRoomMemberSerializer(chatRoomMember, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateMessage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            chat_room = serializer.validated_data['chat_room_id']
            content = serializer.validated_data['content']
            receiver = serializer.validated_data.get('receiver')
            key_id = serializer.validated_data['key_id']
            
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                chat_room=chat_room,
                content=content,
                key_id=key_id
            )
            return Response(
                {'message_id': str(message.id)}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetMessage(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        chat_room_id = request.query_params.get('chat_room_id')
        chatRoom = ChatRoom.objects.get(id=chat_room_id)
        messages = Message.objects.filter(
            chat_room=chatRoom, 
            receiver=request.user,
        ).order_by('created_at')
        serializer = GetMessageSerializer(messages, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

