from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.model.crud.channel import create_channel, read_channel, read_channels, delete_channel, update_channel
from app.model.database import get_db

router = APIRouter(prefix='/channel', tags=['channel'])


@router.post('/')
async def channel_create(channel_name: str = "Untitled", db: Session = Depends(get_db())):
    # TODO: Connect to db.
    # TODO: 1. Input channel information to db.

    channel = await create_channel(db=db, channel_name=channel_name)

    # TODO: 2. Return channel information.
    return {
        'success': True,
        'channel': channel
    }


@router.get('/')
async def channel_read_by_name(channel_name: str, db: Session = Depends(get_db())):
    channel = await read_channel(db=db, channel_name=channel_name)

    return {'read_channel': True,
            'channel': channel}


@router.get('/')
async def channel_read(db: Session = Depends(get_db())):
    all_channel = await read_channels(db=db)
    return {'all_channel': all_channel}


@router.patch('/')
async def channel_update(new_channel_name: str, old_channel_name: str, db: Session = Depends(get_db())):
    channel_updated = await update_channel(db=db, new_channel_name=new_channel_name, old_channel_name=old_channel_name)
    return {'channel updated': True,
            'channel': channel_updated}


@router.delete('/')
async def delete_channel(channel_name: str, db: Session = Depends(get_db())):
    if channel_name:
        raise HTTPException(status_code=404, detail="channel_name not found")
    deleted_channel = await delete_channel(channel_name, db=db)
    return {"deleted": True,
            "deleted_channel": deleted_channel
            }
