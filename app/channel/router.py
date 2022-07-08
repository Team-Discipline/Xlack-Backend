from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.model.crud.channel import create_channel
from app.model.database import get_db

router = APIRouter(prefix='/channel', tags=['channel'])


# Channels

@router.post('/')
async def channel_create(channel_name: str = "Untitled", db: Session = Depends(get_db)):
    # TODO: Connect to db.
    # TODO: 1. Input channel information to db.

    channel = await create_channel(db=db, channel_name=channel_name)

    # TODO: 2. Return channel information.
    return {
        'success': True,
        'channel': channel
    }


# @router.get('/create_channel/{channel_member}')
# async def get_channel_info(member_name: str):
#     return {member_name}


@router.get('/info/{channel_info}')
async def get_channel_feature(channel_info: str):
    return {
        'sdlfkj': channel_info
    }


# FIXME: 의도 모르겠음.
# TODO: 삭제
@router.get('/create_channel/channel_info/{channel_date}')
async def get_channel_datetime(date: datetime):
    return date


# FIXME: Change to update.
@router.put('/create_channel/{channel_info}')
async def update_channel(new_channel_name: str, update_date: datetime):
    get_channel_info.channel_name = new_channel_name
    get_channel_info.channel_date = update_date
    return {get_channel_info}


# TODO: Don't need to use `create_channel`.
# FIXME: Refactoring.
@router.delete('/create_channel/{channel_info}')
async def delete_channel_info(member_name: str):
    member_name = get_channel_info.get(member_name)
    if member_name not in get_channel_info():
        raise HTTPException(status_code=404)
    get_channel_info.delete(member_name)
    get_channel_info.commit()
    return {"deleted": True}


# chats

# FIXME: Refactoring.
class Chat(BaseModel):
    chatter: str
    content: str
    date: datetime


# FIXME: Change method.
# FIXME: Delte create keyword
@router.get('/create_chat', response_model=Chat)
async def create_chat(chat: Chat):
    return chat


# FIXME: Remove `create` keyword.
# TODO: Refactoring.
@router.get('/create_chat/{show_chat}')
async def show_chat(chat: Chat):
    return {"content": chat.content,
            "chatter": chat.chatter,
            "date": chat.date}


# FIXME: remove create.
@router.delete('/create_chat')
async def delete_chat(chat: Chat):
    if chat not in chat:  # if not chat: /
        raise HTTPException(status_code=404, detail="404 chat not found")
    create_chat.delete(Chat)
    create_chat.commit()
    return {"chat deleted": True}
