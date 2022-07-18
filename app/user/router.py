import logging
from datetime import timedelta

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..errors.jwt_error import RefreshTokenExpired, AccessTokenExpired
from ..model.crud import authorization
from ..model.crud.authorization import read_authorization
from ..model.crud.user import read_users, read_user, update_user, delete_user, create_user
from ..model.database import get_db
from ..model.schemas import UserCreate, UserUpdate
from ..utils.jwt import issue_token, check_auth_using_token
from ..utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/')
async def user_create(user_info: UserCreate,
                      db: Session = Depends(get_db)):
    logging.info('POST /user/')

    # Check authorization first!
    if not await authorization.read_authorization(name=user_info.authorization, db=db):
        logging.debug('No such authorization.')
        raise HTTPException(status_code=404, detail='No such authorization.')

    # If authorization exists, create user
    try:
        created_user = await create_user(github_id=str(user_info.github_id),
                                         email=user_info.email,
                                         name=user_info.name,
                                         authorization_name=user_info.authorization,
                                         refresh_token=None,
                                         thumbnail_url=user_info.thumbnail_url,
                                         db=db)
        logging.debug(f'user created: {created_user}')
    except sqlalchemy.exc.IntegrityError as e:
        logging.warning(f'IntegrityError: {e}')
        return FailureResponse(message=e.args[0].split('\"')[1], status_code=400)

    user = await read_user(db=db, user_id=created_user.user_id)
    print(f'user: {user}')
    logging.debug(f'user: {user}')

    # And then, Issue access_token and refresh_token.
    user = {
        'user_id': user.user_id,
        'email': user.email,
        'name': user.name,
        'authorization': user.authorization,
        'created_at': str(user.created_at),
        'thumbnail_url': user.thumbnail_url
    }  # This code is inevitable to convert to `dict` object. Fucking `datetime` is not json parsable.
    access_token = issue_token(user_info=user, delta=timedelta(hours=1))
    refresh_token = issue_token(user_info=user, delta=timedelta(days=14))

    # And then, Update user info with `refresh_token`.
    updated_user = await update_user(db=db,
                                     user_id=str(user['user_id']),
                                     email=user['email'],
                                     name=user['name'],
                                     authorization_name=user['authorization'],
                                     thumbnail_url=user['thumbnail_url'],
                                     refresh_token=refresh_token)
    logging.debug(f'updated user: {updated_user}')

    return SuccessResponse(message='Successfully created user.',
                           user=updated_user.to_dict(),
                           access_token=access_token,
                           refresh_token=refresh_token)


@router.get('/')
async def user_read(user_id: str,
                    token_payload: dict = Depends(check_auth_using_token),
                    db: Session = Depends(get_db)):
    """
    When you want to get user info from database.
    You must input `user_id` or `email`. One of them!
    The tokens are just needed to be valid.
    Don't check who's token.
    """
    logging.info('GET /user/')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return JSONResponse(content={
            'success': False,
            'detail': token_payload.detail
        }, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('this user has admin authorization.')
        raise HTTPException(detail='Not enough authorization to do this.', status_code=status.HTTP_401_UNAUTHORIZED)

    result = await read_user(user_id=user_id, db=db)
    logging.debug(f'user: {result}')

    if result is not None:
        return SuccessResponse(user=result)
    else:
        return FailureResponse(message='No such user.', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/all')
async def get_all_users(token_payload: dict = Depends(check_auth_using_token),
                        db: Session = Depends(get_db)):
    """
    Only `admin` authorization can get this endpoint.
    """
    logging.info('GET /user/all')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return JSONResponse(content={
            'success': False,
            'detail': token_payload.detail
        }, status_code=token_payload.status_code)

    auth = token_payload['authorization']
    if auth != 'admin':
        logging.debug('this user has admin authorization.')
        raise HTTPException(detail='Not enough authorization to do this.', status_code=status.HTTP_401_UNAUTHORIZED)

    users = await read_users(db)
    logging.debug(f'users: {users}')

    if users is not None:
        return SuccessResponse(user=users)
    else:
        return FailureResponse(message='No users.', status_code=status.HTTP_404_NOT_FOUND)


@router.patch('/{user_id}')
async def update_user_info(user_info: UserUpdate,
                           token_payload: dict = Depends(check_auth_using_token),
                           user_id: str | None = Path(default=None, description='One of way to select user.'),
                           db: Session = Depends(get_db)):
    """
    When you want to update user's information.
    Put user information you want to update on **request body**.
    Use `user_id`.
    """
    logging.info('PATCH /user/')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return JSONResponse(content={
            'success': False,
            'detail': token_payload.detail
        }, status_code=token_payload.status_code)

    # To update user's information, Be admin or client itself.
    auth = token_payload['authorization']
    client_user_id = token_payload['user_id']
    if auth != 'admin' or user_id != client_user_id:
        logging.debug('client hasn\'t admin authorization or user_id is not correct.')
        raise HTTPException(detail='No authorization to do this.', status_code=status.HTTP_401_UNAUTHORIZED)

    # Check authorization first.
    if not await read_authorization(user_info.authorization, db):
        logging.debug('No such authorization.')
        raise HTTPException(status_code=404, detail='No such authorization.')

    # If authorization exists, Fix user information.
    rows = await update_user(db=db, user_id=user_id,
                             email=user_info.email,
                             name=user_info.name,
                             thumbnail_url=user_info.thumbnail_url,
                             authorization_name=user_info.authorization,
                             refresh_token=user_info.refresh_token)

    if not rows:
        logging.debug('Not updated.')
        return FailureResponse(message='Not updated.', status_code=status.HTTP_403_FORBIDDEN)
    else:
        return SuccessResponse(message='Successfully updated.', user=await read_user(db=db, user_id=user_id))


@router.delete('/')
async def remove_user(user_id: str,
                      token_payload: dict = Depends(check_auth_using_token),
                      db: Session = Depends(get_db)):
    logging.info('DELETE /user/')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    auth = token_payload['authorization']
    client_user_id = token_payload['user_id']
    if auth != 'admin' or user_id != client_user_id:
        logging.debug('No authorization to do this.')
        return FailureResponse(message='No authorization to do this.', status_code=status.HTTP_401_UNAUTHORIZED)

    rows = await delete_user(user_id=user_id, db=db)
    logging.debug(f'deleted count: {rows}')

    if not rows:
        logging.debug('Not deleted.')
        return FailureResponse(message='Not deleted.', status_code=status.HTTP_404_NOT_FOUND)

    return SuccessResponse(message='Successfully deleted.', count=rows)
