import uuid

from sqlalchemy.orm import Session

from app.model import models
from fastapi import HTTPException

async def create_channel(db: Session, channel_name: str) -> models.Channel:
    channel = models.Channel(uuid=str(uuid.uuid4()), channel_name=channel_name)

    db.add(channel)
    db.commit()
    db.refresh(channel)

    return channel


async def read_channel(db: Session, channel_name: str) -> str:
    channel = models.Channel(uuid=str(uuid.uuid4()), channel_name=channel_name)
    # db.refresh(channel)
    return db.get(channel, channel_name)


async def read_channels(db: Session) -> [models.Channel]:
    return db.query(models.Channel).all()

async def update_channel(db: Session) -> int:
    return None


async def delete_channel(db: Session, channel_name: str) -> int:
    channel_deleted = db.query(models.Channel).filter_by(channel_name=channel_name)
    db.delete(channel_deleted)
    db.commit()
    await update_channel(db=db)

    return channel_deleted
