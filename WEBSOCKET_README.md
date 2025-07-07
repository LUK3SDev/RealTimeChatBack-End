# WebSocket Chat Implementation

This document describes the WebSocket implementation for real-time chat functionality in the Django Channels-based chat application.

## Overview

The WebSocket implementation provides real-time messaging capabilities with the following features:

- **Authentication**: Token-based authentication using Django REST Framework tokens
- **Room-based messaging**: Messages are sent to specific chat rooms
- **Database persistence**: All messages are automatically saved to the database
- **User verification**: Only chat room members can connect and send messages
- **Error handling**: Comprehensive error handling with proper WebSocket close codes

## WebSocket Endpoint

### URL Pattern
```ws://localhost:8000/ws/chat/{chat_room_id}/?token={auth_token}
```

### Parameters
- `chat_room_id`: UUID of the chat room to connect to
- `token`: Authentication token (passed as query parameter)

## Connection Flow

1. **Authentication**: Client connects with a valid authentication token
2. **Membership Verification**: System verifies user is a member of the chat room
3. **Group Join**: User is added to the chat room's WebSocket group
4. **Connection Confirmation**: Server sends connection confirmation message

## Message Format

### Sending Messages
```json
{
    "type": "chat_message",
    "message": "Hello, world!",
    "receiver_id": "optional-user-uuid"
}
```

### Receiving Messages
```json
{
    "type": "chat_message",
    "message": "Hello, world!",
    "sender_id": "sender-uuid",
    "sender_username": "sender_username",
    "message_id": "message-uuid",
    "timestamp": "2024-01-01T12:00:00Z",
    "receiver_id": "receiver-uuid"
}
```

### Connection Confirmation
```json
{
    "type": "connection_established",
    "message": "Connected to chat room {chat_room_id}",
    "user_id": "user-uuid",
    "username": "username"
}
```

### Error Messages
```json
{
    "type": "error",
    "message": "Error description"
}
```

## WebSocket Close Codes

- `4001`: Unauthorized (invalid or missing token)
- `4003`: Not a member of the chat room
- `1000`: Normal closure

## Implementation Details

### ChatConsumer Class

The main WebSocket consumer is located in `chat/consumers.py` and provides:

- **Async WebSocket handling**: Uses Django Channels' AsyncWebsocketConsumer
- **Database operations**: Async database operations using `@database_sync_to_async`
- **Token verification**: Validates Django REST Framework tokens
- **Message persistence**: Automatically saves messages to the database
- **Group messaging**: Broadcasts messages to all room members

### Key Methods

- `connect()`: Handles WebSocket connection with authentication
- `disconnect()`: Handles WebSocket disconnection
- `receive()`: Processes incoming messages
- `chat_message()`: Broadcasts messages to room members
- `verify_token()`: Validates authentication tokens
- `verify_chat_room_membership()`: Checks if user is a room member
- `save_message()`: Persists messages to the database

## Testing

### Using the Test Script

1. Update the configuration in `websocket_test.py`:
   ```python
   CHAT_ROOM_ID = "your-actual-chat-room-uuid"
   AUTH_TOKEN = "your-actual-auth-token"
   ```

2. Run the test script:
   ```bash
   python websocket_test.py
   ```

### Manual Testing with JavaScript

```javascript
// Connect to WebSocket
const ws = new WebSocket(
    `ws://localhost:8000/ws/chat/${chatRoomId}/?token=${authToken}`
);

// Handle connection open
ws.onopen = function(event) {
    console.log('Connected to WebSocket');
};

// Handle incoming messages
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

// Send a message
ws.send(JSON.stringify({
    type: 'chat_message',
    message: 'Hello from JavaScript!',
    receiver_id: null
}));

// Handle connection close
ws.onclose = function(event) {
    console.log('WebSocket closed:', event.code, event.reason);
};
```

## Configuration

### Django Settings

The WebSocket functionality requires the following Django settings:

```python
# In settings.py
INSTALLED_APPS = [
    # ... other apps
    'channels',
    'chat',
    'account'
]

# ASGI application
ASGI_APPLICATION = 'real_time_chat_backend.asgi.application'

# Channel layer (for development)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
```

### Production Considerations

For production, consider:

1. **Redis Channel Layer**: Replace InMemoryChannelLayer with Redis
2. **HTTPS/WSS**: Use secure WebSocket connections
3. **Load Balancing**: Configure load balancers for WebSocket support
4. **Monitoring**: Add logging and monitoring for WebSocket connections

## Security Features

- **Token Authentication**: All connections require valid authentication tokens
- **Room Membership**: Users can only connect to rooms they're members of
- **Input Validation**: All incoming messages are validated
- **Error Handling**: Proper error responses without exposing sensitive information

## Error Handling

The implementation includes comprehensive error handling:

- **Invalid JSON**: Returns error message for malformed JSON
- **Database Errors**: Handles database connection and query errors
- **Authentication Errors**: Proper WebSocket close codes for auth failures
- **Room Access Errors**: Validates room membership before allowing connections

## Dependencies

- Django Channels
- Django REST Framework (for token authentication)
- PostgreSQL (for message storage)
- Redis (recommended for production channel layer) 