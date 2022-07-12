import uuid

from sqlalchemy.orm import Session

from app.model import models


async def create_chat(db: Session,
                      chat_id: int,
                      chat_content: str,
                      chatter: str):
    chat = models.Chat(uuid=int(uuid.uuid4()), chat_id=chat_id,
                       chat_content=chat_content, chatter_name=chatter)

    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


async def read_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter_by(chat_id=chat_id)


async def read_chats(db: Session):
    return db.query(models.Chat).all()


async def update_chat(db: Session, old_chat_content: str, new_chat_content: str):
    # chat_updated = models.Chat(uuid=int(uuid.uuid4()),
    #                            chat_id=chat_id,
    #                            chat_content=new_chat_content)
    chat_updated = db.query(models.Chat). \
        filter(models.Chat.chat_content == old_chat_content).update({'new_chat_content': new_chat_content})
    db.commit()
    return chat_updated


async def delete_chat(db: Session, chat_id: int):
    chat_deleted = db.query(models.Chat).filter_by(chat_id=chat_id)
    db.delete(chat_deleted)
    db.commit()
    db.refresh(chat_deleted)

    return chat_deleted
