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
    return db.query(models.Channel).filter_by(channel_name=channel_name)


async def read_channels(db: Session) -> [models.Channel]:
    return db.query(models.Channel).all()


async def update_channel(db: Session, old_channel_name: str, new_channel_name: str) -> int:
    channel_update = db.query(models.Channel). \
        filter(models.Channel.name == old_channel_name).update({'name': new_channel_name})
    db.commit()
    return channel_update


async def delete_channel(db: Session, channel_name: str) -> int:
    channel_deleted = db.query(models.Channel).filter_by(channel_name=channel_name)
    db.delete(channel_deleted)
    db.commit()
    await update_channel(db=db)
    return channel_deleted
