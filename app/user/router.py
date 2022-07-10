from datetime import timedelta

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..errors.jwt_error import RefreshTokenExpired, AccessTokenExpired
from ..model.crud import user, authorization
from ..model.crud.authorization import read_authorization
from ..model.crud.user import read_users, read_user, update_user, delete_user
from ..model.database import get_db
from ..model.schemas import UserCreate, UserUpdate
from ..utils.jwt import issue_token, check_auth_using_token

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/')
async def create_user(user_info: UserCreate,
                      db: Session = Depends(get_db)):
    # Check authorization first!
    if not await authorization.read_authorization(name=user_info.authorization, db=db):
        raise HTTPException(status_code=404, detail='No such authorization.')

    # And then, Issue access_token and refresh_token.
    access_token = issue_token(user_info=dict(user_info), delta=timedelta(hours=1))
    refresh_token = issue_token(user_info=dict(user_info), delta=timedelta(days=14))

    # If authorization exists, create user
    try:
        await user.create_user(github_id=str(user_info.github_id),
                               email=user_info.email,
                               name=user_info.name,
                               authorization_name=user_info.authorization,
                               refresh_token=refresh_token,
                               thumbnail_url=user_info.thumbnail_url,
                               db=db)
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(detail=e.args[0].split('\"')[1], status_code=400)

    return {
        'success': True,
        'message': 'Successfully created user.',
        'user': await read_user(db=db, email=user_info.email),
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@router.get('/')
async def read_user_info(payload: dict = Depends(check_auth_using_token),
                         user_id: str | None = None,
                         email: str | None = None,
                         db: Session = Depends(get_db)):
    """
    When you want to get user info from database.
    You must input `user_id` or `email`. One of them!

    :param payload:
    :param user_id:
    :param email:
    :param db:
    :return:
    """
    if isinstance(payload, RefreshTokenExpired) or isinstance(payload, AccessTokenExpired):
        return JSONResponse(content={
            'success': False,
            'detail': payload.detail
        }, status_code=payload.status_code)

    result = await read_user(user_id=user_id, email=email, db=db)

    return {
        'success': True,
        'user': result
    } if result is not None else JSONResponse(content={
        'success': False,
        'message': 'No such user.'
    }, status_code=404)


@router.get('/all')
async def get_all_users(payload: dict = Depends(check_auth_using_token),
                        db: Session = Depends(get_db)):
    if isinstance(payload, RefreshTokenExpired) or isinstance(payload, AccessTokenExpired):
        return JSONResponse(content={
            'success': False,
            'detail': payload.detail
        }, status_code=payload.status_code)

    users = await read_users(db)
    return {
        'success': True,
        'users': users
    } if len(users) != 0 else JSONResponse(content={
        'success': False,
        'message': 'No users.'
    }, status_code=404)


@router.patch('/')
async def update_user_info(user_info: UserUpdate,
                           payload: dict = Depends(check_auth_using_token),
                           user_id: str | None = Query(default=None, description='One of way to select user.'),
                           db: Session = Depends(get_db)):
    """
    When you want to update user's information.
    Put user information you want to update on **request body**.
    Use `user_id`.

    :param user_info:
    :param user_id:
    :param db:
    :return:
    """
    if isinstance(payload, RefreshTokenExpired) or isinstance(payload, AccessTokenExpired):
        return JSONResponse(content={
            'success': False,
            'detail': payload.detail
        }, status_code=payload.status_code)

    # Check authorization first.
    if not await read_authorization(user_info.authorization, db):
        raise HTTPException(status_code=404, detail='No such authorization.')

    # If authorization exists, Fix user information.
    rows = await update_user(db=db, user_id=user_id,
                             email=user_info.email,
                             name=user_info.name,
                             thumbnail_url=user_info.thumbnail_url,
                             authorization_name=user_info.authorization,
                             refresh_token=user_info.refresh_token)

    if not rows:
        raise HTTPException(detail='Not updated.')

    return {
        'success': True,
        'message': 'Successfully updated.',
        'user': await read_user(db=db, user_id=user_id)
    }


# TODO: Check authorization. (whether admin or member)
@router.delete('/')
async def remove_user(user_id: str,
                      payload: dict = Depends(check_auth_using_token),
                      db: Session = Depends(get_db)):
    if isinstance(payload, RefreshTokenExpired) or isinstance(payload, AccessTokenExpired):
        return JSONResponse(content={
            'success': False,
            'detail': payload.detail
        }, status_code=payload.status_code)

    rows = await delete_user(user_id=user_id, db=db)

    if not rows:
        raise HTTPException(detail='Not deleted.', status_code=404)

    return {
        'success': True,
        'message': 'Successfully deleted.',
        'count': rows
    }
