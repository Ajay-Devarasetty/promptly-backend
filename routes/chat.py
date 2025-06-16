# routes/chat.py

from fastapi import APIRouter, HTTPException
from models.chat import Chat, ChatEntry
from typing import List
from controllers.chat import save_chat, get_chats_by_user

router = APIRouter(
    prefix="/chats",
    tags=["CHATS"]
)

#------------------------------------------------------------------------------------------------------------------------

@router.post("/chat")
async def create_chat(chat: Chat):
    return await save_chat(chat)

#-----------------------------------------------------------------------------------------------------------------


@router.get("/user/{user_id}", response_model=List[ChatEntry])
def fetch_chats(user_id: str):
    return get_chats_by_user(user_id)