from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, File, HTTPException
from datetime import datetime

router = APIRouter(prefix='/channel', tags=['channel'])


# Channels

@router.get('/create_channel')
async def get_channel_info(channel_id: int, channel_date: datetime, channel_name: str | None = Query(defalt="unnamed")):
    return {"channel_id": channel_id,
            "channel_name": channel_name,
            "channel_date": channel_date}


@router.get('/create_channel/{channel_member}')
async def get_channel_info(member_name: str):
    return {member_name}


@router.get('/create_channel/channel_info/{channel_feature}')
async def get_channel_feature(feature: None):
    return feature


@router.get('/create_channel/channel_info/{channel_date}')
async def get_channel_datetime(date: datetime):
    return date


@router.put('/create_channel/{channel_info}')
async def update_channel(new_channel_name: str, update_date: datetime):
    get_channel_info.channel_name = new_channel_name
    get_channel_info.channel_date = update_date
    return {get_channel_info}


@router.delete('/create_channel/{channel_info}')
async def delete_channel_info(member_name: str):
    member_name = get_channel_info.get(member_name)
    if member_name not in get_channel_info():
        raise HTTPException(status_code=404)
    get_channel_info.delete(member_name)
    get_channel_info.commit()
    return {"deleted": True}


# chats

class Chat(BaseModel):
    chatter: str
    content: str
    date: datetime


@router.get('/create_chat', response_model=Chat)
async def create_chat(chat: Chat):
    return chat


@router.get('/create_chat/{show_chat}')
async def show_chat(chat: Chat):
    return {"content": chat.content,
            "chatter": chat.chatter,
            "date": chat.date}


@router.delete('/create_chat')
async def delete_chat(chat: Chat):
    if chat not in chat:
        raise HTTPException(status_code=404, detail="404 chat not found")
    create_chat.delete(Chat)
    create_chat.commit()
    return {"chat deleted": True}
