import uuid

from sqlalchemy import Column, String, Integer, TIMESTAMP, func, ForeignKey

from .database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), autoincrement=True, unique=True, primary_key=True, nullable=False)
    uuid = Column(String(50), unique=True, nullable=False)

    github_id = Column(String(100), unique=True, nullable=True)

    email = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), nullable=True)

    # `func.now()` means `TIMESTAMP.NOW()`.
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

    authorization = Column(String(25), ForeignKey('authorizations.name'))

    refresh_token = Column(String(1000), unique=True, nullable=True)

    thumbnail_url = Column(String(500), nullable=True)


class Authorization(Base):
    __tablename__ = 'authorizations'

    uuid = Column(String(50), nullable=False, primary_key=True, default=uuid.uuid4())
    name = Column(String(25), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())


class Channel(Base):
    __tablename__ = 'channels'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    channel_id = Column(Integer, autoincrement=True, unique=True)
    channel_name = Column(String(50))
    created_at = Column(TIMESTAMP(), defualt=func.now())


class Chat(Base):
    __tablename__ = 'chats'

    uuid = Column(Integer, primary_key=True, unique=True)
    chat_id = Column(Integer, autoincrement=True, unique=True)
    chat_content = Column(String(1000))
    chatter_name = Column(String(50))
    create_at = Column(TIMESTAMP(), default=func.now())
