from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from .models import Message, ChatRoom
from .database import Message as MessageDB, ChatRoom as ChatRoomDB
from .websocket import handle_websocket
from ..auth.dependencies import get_current_user

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await handle_websocket(websocket, user_id)

@router.get("/messages/{receiver_id}", response_model=List[Message])
async def get_messages(
    receiver_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(MessageDB).filter(
        ((MessageDB.sender_id == current_user["id"]) & (MessageDB.receiver_id == receiver_id)) |
        ((MessageDB.sender_id == receiver_id) & (MessageDB.receiver_id == current_user["id"]))
    ).order_by(MessageDB.created_at.desc()).offset(skip).limit(limit).all()
    
    return messages

@router.get("/chat-rooms", response_model=List[ChatRoom])
async def get_chat_rooms(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_rooms = db.query(ChatRoomDB).filter(
        (ChatRoomDB.user1_id == current_user["id"]) |
        (ChatRoomDB.user2_id == current_user["id"])
    ).all()
    
    return chat_rooms

@router.post("/chat-rooms/{user_id}", response_model=ChatRoom)
async def create_chat_room(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if chat room already exists
    existing_room = db.query(ChatRoomDB).filter(
        ((ChatRoomDB.user1_id == current_user["id"]) & (ChatRoomDB.user2_id == user_id)) |
        ((ChatRoomDB.user1_id == user_id) & (ChatRoomDB.user2_id == current_user["id"]))
    ).first()
    
    if existing_room:
        return existing_room
    
    # Create new chat room
    chat_room = ChatRoomDB(
        user1_id=current_user["id"],
        user2_id=user_id
    )
    db.add(chat_room)
    db.commit()
    db.refresh(chat_room)
    
    return chat_room

@router.put("/messages/{message_id}/read")
async def mark_message_as_read(
    message_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(MessageDB).filter(
        MessageDB.id == message_id,
        MessageDB.receiver_id == current_user["id"]
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    db.commit()
    
    return {"status": "success"} 