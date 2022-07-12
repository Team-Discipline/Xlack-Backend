from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.model.crud.chat import create_chat, read_chat, read_chats, update_chat, delete_chat
from app.model.database import get_db

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/')
async def chat_create(chat_id: int, chat_content: str,
                      chatter: str, db: Session = Depends(get_db)):
    chat = await create_chat(chat_id=chat_id, chat_content=chat_content,
                             chatter=chatter, db=db)
    return {
        'success': True,
        'chat': chat
    }


@router.get('/')
async def show_chat_by_id(chat_id: int, db: Session = Depends(get_db)):
    chat = await read_chat(chat_id=chat_id, db=db)
    if chat_id:
        raise HTTPException(status_code=404, detail="404 chat_id not found")
    else:
        return {'success': True,
                'chat': chat}


@router.get('/every')
async def show_chat_all(db: Session = Depends(get_db)):
    all_chat = await read_chats(db=db)
    return {'success': True,
            'all_chat': all_chat}


@router.patch('/')
async def chat_update(chat_id: int, new_chat_content: str, db: Session = Depends(get_db)):
    updated_chat = await update_chat(new_chat_content=new_chat_content, db=db)
    return {'success': True,
            'updated_chat': updated_chat}


@router.delete('/')
async def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat_delete = await delete_chat(chat_id=chat_id, db=db)
    if chat_id:
        raise HTTPException(status_code=404, detail="404 chat_id not found")
    else:
        return {'success': True,
                'chat_deleted': chat_delete}
