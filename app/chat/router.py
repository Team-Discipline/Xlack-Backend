import logging

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from app.errors.jwt_error import AccessTokenExpired, RefreshTokenExpired
from app.model.crud.chat import create_chat, read_chat, read_chats, update_chat, delete_chat
from app.model.database import get_db
from app.model.schemas import Chat, ChatCreate
from app.utils.jwt import check_auth_using_token
from app.utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/', response_model=Chat)
async def chat_create(chat: Chat, db: Session = Depends(get_db)):
    logging.info('POST /chat/')
    db_chat = await create_chat(db, chat_id=chat.chat_id, chat_content=chat.chat_content,
                                chatter=chat.chatter_name)
    logging.debug(f'chat: {chat}')

    return SuccessResponse(message='Successfully Created Chat', chat=db_chat.to_dict())


@router.get('/', response_model=Chat)
async def show_chat_by_id(chat: Chat, chat_id: int, db: Session = Depends(get_db)):
    logging.info('GET /chat/')
    chats = await read_chat(db, chat_id=chat_id)
    if chat_id:
        raise HTTPException(status_code=404, detail="404 chat_id not found")
    else:
        return {'success': True,
                'chat': chats}

    return SuccessResponse(chat=chat.to_dict())

@router.get('/{every}', response_model=Chat)
async def show_chat_all(db: Session = Depends(get_db)):
    logging.info('GET /chat/all')
    all_chat = await read_chats(db)
    logging.debug(f'all chats: {all_chat}')
    return SuccessResponse(chats=[chat.to_dict() for chat in all_chat])



@router.patch('/', response_model=Chat)
async def chat_update(new_chat_content: str, old_chat_content: str, db: Session = Depends(get_db)):
    logging.info('PATCH /channel/')
    updated_chat = await update_chat(db, new_chat_content=new_chat_content, old_chat_content=old_chat_content)
    logging.debug(f'updated chat: {updated_chat}')

    return SuccessResponse(message='Successfully edited chat.', updated_chat=updated_chat.to_dict())

@router.delete('/', response_model=Chat)
async def chat_delete(chat_id: int, db: Session = Depends(get_db)):
    logging.info('DELETE /channel/')
    chat_d = await delete_chat(db, chat_id=chat_id)
    logging.debug(f'deleted chat count: {chat_d}')
    if chat_id:
        raise HTTPException(status_code=404, detail="404 chat_id not found")
    else:
        return {'success': True,
                'chat_deleted': chat_d}
