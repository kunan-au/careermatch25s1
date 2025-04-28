from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy import insert
from ..database import async_session, messages as MessageDB
from .models import Message, MessageType
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.user_rooms: Dict[int, Set[int]] = {}  # user_id -> set of room_ids

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_rooms[user_id] = set()

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str, room_id: int):
        for user_id in self.user_rooms:
            if room_id in self.user_rooms[user_id]:
                await self.send_personal_message(message, user_id)

    def add_user_to_room(self, user_id: int, room_id: int):
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = set()
        self.user_rooms[user_id].add(room_id)

    def remove_user_from_room(self, user_id: int, room_id: int):
        if user_id in self.user_rooms:
            self.user_rooms[user_id].discard(room_id)

manager = ConnectionManager()

async def handle_websocket(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            if message_data["type"] == "text":
                await handle_text_message(message_data, user_id)
            elif message_data["type"] == "file":
                await handle_file_message(message_data, user_id)
            elif message_data["type"] == "join_room":
                await handle_join_room(message_data, user_id)
            elif message_data["type"] == "leave_room":
                await handle_leave_room(message_data, user_id)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"Error in websocket handler: {e}")
        manager.disconnect(user_id)

async def handle_text_message(message_data: dict, sender_id: int):
    async with async_session() as session:
        # Create message in database
        stmt = insert(MessageDB).values(
            sender_id=sender_id,
            receiver_id=message_data["receiver_id"],
            content=message_data["content"],
            message_type=MessageType.TEXT.value,
            created_at=datetime.utcnow()
        )
        result = await session.execute(stmt)
        await session.commit()

        # Prepare message for sending
        message_dict = {
            "id": result.inserted_primary_key[0],
            "sender_id": sender_id,
            "receiver_id": message_data["receiver_id"],
            "content": message_data["content"],
            "type": "text",
            "created_at": datetime.utcnow().isoformat()
        }

        # Send to receiver if online
        await manager.send_personal_message(
            json.dumps(message_dict),
            message_data["receiver_id"]
        )

async def handle_file_message(message_data: dict, sender_id: int):
    async with async_session() as session:
        # Create message in database
        stmt = insert(MessageDB).values(
            sender_id=sender_id,
            receiver_id=message_data["receiver_id"],
            content=message_data["content"],
            message_type=MessageType.FILE.value,
            file_url=message_data.get("file_url"),
            file_name=message_data.get("file_name"),
            created_at=datetime.utcnow()
        )
        result = await session.execute(stmt)
        await session.commit()

        # Prepare message for sending
        message_dict = {
            "id": result.inserted_primary_key[0],
            "sender_id": sender_id,
            "receiver_id": message_data["receiver_id"],
            "content": message_data["content"],
            "type": "file",
            "file_url": message_data.get("file_url"),
            "file_name": message_data.get("file_name"),
            "created_at": datetime.utcnow().isoformat()
        }

        # Send to receiver if online
        await manager.send_personal_message(
            json.dumps(message_dict),
            message_data["receiver_id"]
        )

async def handle_join_room(message_data: dict, user_id: int):
    room_id = message_data["room_id"]
    manager.add_user_to_room(user_id, room_id)
    await manager.send_personal_message(
        json.dumps({
            "type": "room_joined",
            "room_id": room_id
        }),
        user_id
    )

async def handle_leave_room(message_data: dict, user_id: int):
    room_id = message_data["room_id"]
    manager.remove_user_from_room(user_id, room_id)
    await manager.send_personal_message(
        json.dumps({
            "type": "room_left",
            "room_id": room_id
        }),
        user_id
    ) 