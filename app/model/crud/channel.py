import uuid

from sqlalchemy.orm import Session

from app.model import models


async def create_channel(db: Session, channel_name: str) -> models.Channel:
    channel = models.Channel(uuid=str(uuid.uuid4()), channel_name=channel_name)

    db.add(channel)
    db.commit()
    db.refresh(channel)

    return channel


async def read_channel(db: Session, channel_name: str) -> str:
    channel = models.Channel(uuid=str(uuid.uuid4()), channel_name=channel_name)
    # db.get(channel, channel_name)
    # db.commit()
    # db.refresh(channel)
    return db.get(channel, channel_name)


async def read_channels(db: Session) -> [models.Channel]:
    return ''


async def update_channel(db: Session) -> int:
    return None


async def delete_channel(db: Session) -> int:
    return None
