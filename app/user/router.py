import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ..model.crud import user, authorization
from ..model.crud.authorization import read_authorization
from ..model.crud.user import read_users, read_user, update_user, delete_user
from ..model.database import get_db
from ..model.schemas import UserCreate, UserInformation

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/')
async def create_user(user_info: UserCreate,
                      db: Session = Depends(get_db)):
    # Check authorization first!
    if not await authorization.read_authorization(name=user_info.authorization, db=db):
        raise HTTPException(status_code=404, detail='No such authorization.')

    # If authorization exists, create user.
    result = await user.create_user(github_id=user_info.github_id,
                                    email=user_info.email,
                                    name=user_info.name,
                                    authorization_name=user_info.authorization,
                                    db=db)

    return {
        'success': True,
        'message': 'Successfully created user.',
        'user': result
    }


# TODO: Should adjust auth middleware.
@router.delete('/')
async def remove_user(user_id: str, db: Session = Depends(get_db)):
    rows = await delete_user(user_id=user_id, db=db)

    if not rows:
        raise HTTPException(detail='Not deleted.')

    return {
        'success': True,
        'message': 'Successfully deleted.',
        'count': rows
    }
