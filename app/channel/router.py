from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.model.crud.channel import create_channel, read_channel, read_channels, delete_channel
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

@router.get('/')
async def channel_read_by_name(channel_name: str, db: Session = Depends(get_db())):
    channel = await read_channel(db=db, channel_name=channel_name)

    return {'read_channel': True,
            'channel': channel}

@router.get('/')
async def channel_read(db: Session = Depends(get_db())):
    all_channel = await read_channels(db=db)
    return {'all_channel': all_channel}


# @router.get('/info/{channel_info}')
# async def get_channel_feature(channel_info: str):
#     return {
#         'channel_info': channel_info
#     }


# FIXME: Change to update.
@router.update('/')
async def update_channel(new_channel_name: str, update_date: datetime):
    update_channel.channel_name = new_channel_name
    update_channel.channel_date = update_date
    return {update_channel}


# TODO: Don't need to use `create_channel`.
# FIXME: Refactoring.
@router.delete('/')
async def delete_channel(channel_name: str, db: Session = Depends(get_db())):
    deleted_channel = await delete_channel(channel_name, db=db)
    return {"deleted": True,
            "deleted_channel": deleted_channel,
            }


# chats

# FIXME: Refactoring.
class Chat(BaseModel):
    chatter: str
    content: str
    date: datetime


# FIXME: Change method.
# FIXME: Delete create keyword
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
