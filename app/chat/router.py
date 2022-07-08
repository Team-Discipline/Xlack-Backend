from fastapi import APIRouter

router = APIRouter(prefix='/chat', tags=['chat'])


@router.get('/')
async def chat_create():
    return ' '
