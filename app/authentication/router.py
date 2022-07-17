import base64
import json
import os
from datetime import timedelta

from fastapi import APIRouter, Request, Query, Depends, HTTPException, status, Body
from fastapi.responses import RedirectResponse, JSONResponse
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from ..errors.jwt_error import AccessTokenExpired
from ..model.crud.user import update_user, read_user
from ..model.database import get_db
from ..utils.github_auth import exchange_code_for_access_token, get_user_data_from_github
from ..utils.jwt import check_auth_using_token, issue_token, decode

router = APIRouter(prefix='/authentication', tags=['authentication'])


@router.get('/github_login')
async def login_github():
    """
    Get redirect response to GitHub OAuth2.
    Test code for testing backend redirect codes.
    Frontend team may not use this endpoint.

    :return:
    """

    client_id = os.getenv('GITHUB_CLIENT_ID')
    scope = 'read:user'
    url = f'https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}'
    print(f'url: {url}')
    return RedirectResponse(url)


@router.get('/redirect/github')
async def redirect_github(request: Request, code: str):
    """
    This function deal with after redirect from client.

    :return:
    """

    print(f'params: {request.query_params}')
    print(f'code: {code}')
    res = exchange_code_for_access_token(code)

    print(f'res: {res.content}')

    content = str(res.content)

    first_word = content.split('&')[0].split('=')[0]

    if first_word == 'b\'error':
        return {
            'success': False,
            'message': 'Failed to get access token.',
            'detail': content.split('&')[1].split('=')[1]
        }

    access_token = content.split('&')[0].split('=')[1]

    return {
        'success': True,
        'message': 'Successfully get access token from github.',
        'access_token': access_token
    }


@router.get('/user_info/github')
async def get_user_info(github_access_token: str = Query(
    alias='Access Token From Github.',
    title='github access token',
    description='You should input only GITHUB ACCESS TOKEN!!!',
    max_length=50,
    min_length=30)
):
    """
    When you get information from github directly using github access token.

    :param github_access_token:
    :return:
    """

    res = get_user_data_from_github(github_access_token)
    return {
        'success': True,
        'message': 'Successfully get user information from github.',
        'github_info': json.loads(res.content)
    }


@router.post('/revoke_token/{user_id}')
async def revoke_token(user_id: str, db: Session = Depends(get_db)):
    user_info = await read_user(db, user_id=user_id)

    # Check `user_id` is valid first.
    if user_info is None:
        raise HTTPException(detail='No such user', status_code=404)

    try:
        rows = await update_user(db=db, user_id=user_id,
                                 email=user_info.email,
                                 name=user_info.name,
                                 authorization_name=user_info.authorization,
                                 thumbnail_url=user_info.thumbnail_url)
        if not rows:
            raise HTTPException(detail='[Serious] Not updated!', status_code=404)

    except Exception as e:
        raise HTTPException(detail=e.__str__(), status_code=400)

    return {
        'success': True,
        'message': 'Successfully revoked refresh token.'
    }


@router.post('/update/access_token')
async def update_access_token(access_token: str = Body(...),
                              db: Session = Depends(get_db)):
    return await __issue_new_token(timedelta(hours=1), access_token, db)


@router.post('/update/refresh_token')
async def update_refresh_token(refresh_token: str = Body(...),
                               db: Session = Depends(get_db)):
    return await __issue_new_token(timedelta(days=14), refresh_token, db)


async def __issue_new_token(time: timedelta,
                            token: str = Body(...),
                            db: Session = Depends(get_db)):
    """
    Helper function that helps common logic
    """

    # Check whether access token is expired first.
    try:
        decode(token, key='secret_key', algorithms=['HS256'])
        return JSONResponse(content={
            'success': False,
            'message': 'You can this endpoint when only access token is expired.'
        }, status_code=status.HTTP_403_FORBIDDEN)
    except ExpiredSignatureError:
        pass

    # Get payload from expired token.
    payload = token.split(".")[1]
    padded = payload + "=" * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    payload = json.loads(decoded)
    print(f'payload: {payload}')

    # Issue a new thing.
    user = await read_user(db=db, user_id=payload['user_id'])
    payload = {
        'user_id': user.user_id,
        'email': user.email,
        'name': user.name,
        'authorization': user.authorization,
        'created_at': str(user.created_at),
        'thumbnail_url': user.thumbnail_url
    }  # This code is inevitable to convert to `dict` object. Fucking `datetime` is not json parsable.
    token = issue_token(user_info=payload, delta=time)

    return {
        'success': True,
        'message': 'Successfully re-issued access token.',
        'access_token': token
    }
