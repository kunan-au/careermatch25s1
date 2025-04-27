from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy import select
from typing import List
from ..database import async_session, messages as MessageDB, chat_rooms as ChatRoomDB
from .models import Message, ChatRoom
from .websocket import handle_websocket
from ..auth.dependencies import get_current_user

router = APIRouter()

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await handle_websocket(websocket, user_id)

@router.get("/messages/{receiver_id}", response_model=List[Message])
async def get_messages(
    receiver_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: async_session = Depends(get_db)
):
    query = select(MessageDB).where(
        ((MessageDB.c.sender_id == current_user["id"]) & (MessageDB.c.receiver_id == receiver_id)) |
        ((MessageDB.c.sender_id == receiver_id) & (MessageDB.c.receiver_id == current_user["id"]))
    ).order_by(MessageDB.c.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    messages = result.mappings().all()
    return [Message(**msg) for msg in messages]

@router.get("/chat-rooms", response_model=List[ChatRoom])
async def get_chat_rooms(
    current_user: dict = Depends(get_current_user),
    db: async_session = Depends(get_db)
):
    query = select(ChatRoomDB).where(
        (ChatRoomDB.c.user1_id == current_user["id"]) |
        (ChatRoomDB.c.user2_id == current_user["id"])
    )
    
    result = await db.execute(query)
    chat_rooms = result.mappings().all()
    return [ChatRoom(**room) for room in chat_rooms]

@router.post("/chat-rooms/{user_id}", response_model=ChatRoom)
async def create_chat_room(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: async_session = Depends(get_db)
):
    # Check if chat room already exists
    query = select(ChatRoomDB).where(
        ((ChatRoomDB.c.user1_id == current_user["id"]) & (ChatRoomDB.c.user2_id == user_id)) |
        ((ChatRoomDB.c.user1_id == user_id) & (ChatRoomDB.c.user2_id == current_user["id"]))
    )
    
    result = await db.execute(query)
    existing_room = result.mappings().first()
    
    if existing_room:
        return ChatRoom(**existing_room)
    
    # Create new chat room
    insert_stmt = ChatRoomDB.insert().values(
        user1_id=current_user["id"],
        user2_id=user_id
    )
    result = await db.execute(insert_stmt)
    await db.commit()
    
    # Get the created room
    query = select(ChatRoomDB).where(ChatRoomDB.c.id == result.inserted_primary_key[0])
    result = await db.execute(query)
    chat_room = result.mappings().first()
    
    return ChatRoom(**chat_room)

@router.put("/messages/{message_id}/read")
async def mark_message_as_read(
    message_id: int,
    current_user: dict = Depends(get_current_user),
    db: async_session = Depends(get_db)
):
    query = select(MessageDB).where(
        MessageDB.c.id == message_id,
        MessageDB.c.receiver_id == current_user["id"]
    )
    
    result = await db.execute(query)
    message = result.mappings().first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    update_stmt = MessageDB.update().where(
        MessageDB.c.id == message_id
    ).values(is_read=True)
    await db.execute(update_stmt)
    await db.commit()
    
    return {"status": "success"} 