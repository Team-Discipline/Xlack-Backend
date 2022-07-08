import uuid

from sqlalchemy.orm import Session

from app.model import models


async def create_channel(db: Session, channel_name: str) -> models.Channel:
    channel = models.Channel(uuid=str(uuid.uuid4()), channel_name=channel_name)

    db.add(channel)
    db.commit()
    db.refresh(channel)

    return channel


async def read_channel(db: Session) -> models.Channel:
    return ''


async def read_channels(db: Session) -> [models.Channel]:
    return ''


async def update_channel(db: Session) -> int:
    return ''


async def delete_channel(db: Session) -> int:
    return ''
