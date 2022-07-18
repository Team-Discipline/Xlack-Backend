import logging

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.model.crud.chat import create_chat, read_chat, read_chats, update_chat, delete_chat
from app.model.database import get_db
from app.model.schemas import Chat

router = APIRouter(prefix='/chat', tags=['chat'])


# async def chat_auth_check(name: str, auth: Session(get_auth)):
#     check_auth = auth.get(name=Chat.chatter_name, auth=get_auth.name)
#     if name != auth:
#         raise HTTPException(status_code=401, detail='chatter not authorized')
#     return {
#         'auth': check_auth,
#         'success': True
#     }


@router.post('/', response_model=Chat)
async def chat_create(chat: Chat, db: Session = Depends(get_db)):
    logging.info('POST /chat/')
    db_chat = await create_chat(db, chat_id=chat.chat_id, chat_content=chat.chat_content,
                                chatter=chat.chatter_name)
    logging.debug(f'chat: {chat}')
    if db_chat:
        raise HTTPException(status_code=400, detail='chat_id has been used')
    if chat.chat_content is None:
        chat.chat_content = ' '
    return {
        'success': True,
        'chat': db_chat
    }


@router.get('/', response_model=Chat)
async def show_chat_by_id(chat: Chat, chat_id: int, db: Session = Depends(get_db)):
    logging.info('GET /chat/')
    chats = await read_chat(db, chat_id=chat_id)
    if chat_id:
        raise HTTPException(status_code=404, detail="404 chat_id not found")
    else:
        return {'success': True,
                'chat': chats}


@router.get('/{every}', response_model=Chat)
async def show_chat_all(db: Session = Depends(get_db)):
    logging.info('GET /chat/all')
    all_chat = await read_chats(db)
    logging.debug(f'all chats: {all_chat}')
    return {'success': True,
            'all_chat': all_chat}


@router.patch('/', response_model=Chat)
async def chat_update(new_chat_content: str, old_chat_content: str, db: Session = Depends(get_db)):
    logging.info('PATCH /channel/')
    updated_chat = await update_chat(db, new_chat_content=new_chat_content, old_chat_content=old_chat_content)
    logging.debug(f'updated chat: {updated_chat}')
    if old_chat_content:
        raise HTTPException(status_code=404, detail='chat_content not found')
    return {'success': True,
            'updated_chat': updated_chat}


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
