from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.model import models
from app.model.crud.chat import create_chat, read_chat, read_chats, update_chat, delete_chat
from app.model.database import engine
from app.model.database import get_db
from app.model.schemas import Chat
from app.authorization.router import get_auth
router = APIRouter(prefix='/chat', tags=['chat'])
models.Base.metadata.create_all(bind=engine)


async def chat_auth_check(name: str, auth: Session(get_auth)):
    check_auth = auth.get(name=Chat.chatter_name, auth=get_auth.name)
    if name != auth:
        raise HTTPException(status_code=401, detail='chatter not authorized')
    return {
        'auth': check_auth,
        'success': True
    }


@router.post('/', response_model=Chat)
async def chat_create(chat: Chat, db: Session = Depends(get_db)):
    db_chat = await create_chat(db, chat_id=chat.chat_id, chat_content=chat.chat_content,
                                chatter=chat.chatter_name)
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
    chats = await read_chat(db, chat_id=chat_id)
    if chat_id:
        raise HTTPException(status_code=404, detail="404 chat_id not found")
    else:
        return {'success': True,
                'chat': chats}


@router.get('/{every}', response_model=Chat)
async def show_chat_all(db: Session = Depends(get_db)):
    all_chat = await read_chats(db)
    return {'success': True,
            'all_chat': all_chat}


@router.patch('/', response_model=Chat)
async def chat_update(new_chat_content: str, old_chat_content: str, db: Session = Depends(get_db)):
    updated_chat = await update_chat(db, new_chat_content=new_chat_content, old_chat_content=old_chat_content)
    if old_chat_content:
        raise HTTPException(status_code=404, detail='chat_content not found')
    return {'success': True,
            'updated_chat': updated_chat}


@router.delete('/', response_model=Chat)
async def chat_delete(chat_id: int, db: Session = Depends(get_db)):
    chat_d = await delete_chat(db, chat_id=chat_id)
    if chat_id:
        raise HTTPException(status_code=404, detail="404 chat_id not found")
    else:
        return {'success': True,
                'chat_deleted': chat_d}
