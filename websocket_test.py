#!/usr/bin/env python3
"""
Test script for WebSocket chat functionality
Usage: python websocket_test.py
"""

import asyncio
import websockets
import json
import sys

# Configuration
WEBSOCKET_URL = "ws://localhost:8000/ws/chat/{chat_room_id}/?token={token}"
CHAT_ROOM_ID = "your-chat-room-uuid-here"  # Replace with actual chat room ID
AUTH_TOKEN = "your-auth-token-here"  # Replace with actual auth token

async def test_websocket():
    """Test WebSocket connection and messaging"""
    url = WEBSOCKET_URL.format(
        chat_room_id=CHAT_ROOM_ID,
        token=AUTH_TOKEN
    )
    
    try:
        async with websockets.connect(url) as websocket:
            print(f"Connected to WebSocket: {url}")
            
            # Listen for incoming messages
            async def receive_messages():
                try:
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        print(f"Received: {data}")
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed")
            
            # Start receiving messages in background
            receive_task = asyncio.create_task(receive_messages())
            
            # Send a test message
            test_message = {
                "type": "chat_message",
                "message": "Hello from WebSocket test!",
                "receiver_id": None  # Optional: specific user ID for private
            }
            
            await websocket.send(json.dumps(test_message))
            print(f"Sent: {test_message}")
            
            # Keep connection alive for a few seconds
            await asyncio.sleep(5)
            
            # Cancel the receive task
            receive_task.cancel()
            
    except websockets.exceptions.InvalidURI:
        print("Invalid WebSocket URL")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if (CHAT_ROOM_ID == "your-chat-room-uuid-here" or 
            AUTH_TOKEN == "your-auth-token-here"):
        print("Please update CHAT_ROOM_ID and AUTH_TOKEN in the script")
        print("You can get these from your Django admin or API endpoints")
        sys.exit(1)
    
    asyncio.run(test_websocket()) 