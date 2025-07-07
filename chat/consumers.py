# chat_backend/chat_app/consumers.py

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import ChatRoom, Message, ChatRoomMember
from account.models import UserPublicKey 

logger = logging.getLogger(__name__)
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection with authentication"""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        print(self.room_name)
        print(self.room_group_name)
        
        # Get token from query parameters
        query_string = self.scope.get('query_string', b'').decode()
        query_params = dict(x.split('=') for x in query_string.split('&') if x)
        token = query_params.get('token', '')
        
        # Verify token and get user
        self.user = await self.verify_token(token)
        if not self.user:
            await self.close(code=4001, reason="Unauthorized")
            return
        
        # Verify user is member of the chat room
        is_member = await self.verify_chat_room_membership(
            self.room_name
        )
        if not is_member:
            await self.close(
                code=4003, 
                reason="Not a member of this chat room"
            )
            return
        
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected to chat room {self.room_name}',
            'user_id': str(self.user.id),
            'username': self.user.username
        }))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        logger.info(
            f"User {self.user.username} disconnected from {self.room_name}"
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')
            content = text_data_json.get('message', '')['content']
            receiver_id = text_data_json.get('receiver_id')
            key_id = text_data_json.get('key_id')


            print(message_type)
            print(content)
            print(receiver_id)
            
            if message_type == 'chat_message':
                # Save message to database
                message = await self.save_message(content, receiver_id)
                print('Sono entrato dentro chat_message')
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',  # chiama il metodo chat_message su tutti i consumer del gruppo
                        'message': content,
                        'sender': str(self.user.username),
                        'receiver_id': receiver_id,
                        'created_at': message.created_at.isoformat(),
                        'key_id': key_id,
                        'id': str(message.id)
                    }
                )
            else:
                # Handle other message types
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))

    async def chat_message(self, event):
        """Send chat message to WebSocket"""
        print(event)
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'type': 'chat_message',
            'message': event['message'],
            'sender': json.dumps({
                'username': event['sender']
            }),
            'created_at': event['created_at'],
            'receiver': json.dumps({
                'username': event.get('receiver_id')
            }),
            'key_id': event.get('key_id')
        }))

    @database_sync_to_async
    def verify_token(self, token):
        """Verify authentication token and return user"""
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def verify_chat_room_membership(self, room_name):
        """Verify user is a member of the chat room"""
        try:
            chat_room = ChatRoom.objects.get(id=room_name)
            return ChatRoomMember.objects.filter(
                user=self.user, 
                chat_room=chat_room
            ).exists()
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content, receiver_id=None):
        """Save message to database"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_name)
            receiver = None
            receiverKeyId = None
            
            if receiver_id:
                try:
                    receiver = User.objects.get(username=receiver_id)
                    receiverKeyId = UserPublicKey.objects.get(user=receiver).key_id
                except User.DoesNotExist:
                    pass
            
            message = Message.objects.create(
                sender=self.user,
                receiver=receiver,
                chat_room=chat_room,
                content=content,
                key_id=receiverKeyId
            )
            return message
        except ChatRoom.DoesNotExist:
            raise Exception("Chat room not found")