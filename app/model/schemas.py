import numbers

from pydantic import BaseModel, validator
from datetime import datetime
from .crud.authorization import read_authorizations, read_authorization


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    github_id: str
    authorization: str

    @validator('github_id')
    def check_github_id_is_number(cls, v):
        int(v)
        return v


class UserInformation(UserBase):
    authorization: str


class UserUpdate(UserInformation):
    refresh_token: str


class User(UserBase):
    user_id: int
    uuid: str

    created_at: datetime

    refresh_token: str

    class Config:
        orm_mode = True


"""

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), autoincrement=True, unique=True, primary_key=True, nullable=False)
    uuid = Column(String(25), unique=True, nullable=False)

    github_id = Column(String(100), unique=True, nullable=True)

    email = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), unique=False, nullable=True)

    # `func.now()` means `TIMESTAMP.NOW()`.
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

    authorization = Column(String(25), ForeignKey('authorizations.name'))

"""


class AuthorizationBase(BaseModel):
    name: str


class Authorization(AuthorizationBase):
    uuid: str
    created_at: datetime

    class Config:
        orm_mode = True


"""

class Authorization(Base):
    __tablename__ = 'authorizations'

    uuid = Column(String(25), unique=True, nullable=False, primary_key=True)
    name = Column(String(25), nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

"""
