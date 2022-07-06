from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.model.crud.authorization import read_authorization, delete_authorization, update_authorization, \
    create_authorization, read_authorizations
from app.model.database import get_db

router = APIRouter(prefix='/authorization', tags=['authorization'])


@router.post('/')
async def create_auth(name: str = Query(max_length=25), db: Session = Depends(get_db)):
    auth = await read_authorization(name, db)
    if auth:
        return {
            'success': True,
            'message': 'Already exists.',
            'authorization': auth
        }
    else:
        auth = await create_authorization(name, db)
        return {
            'success': True,
            'message': 'Successfully authorization created.',
            'authorization': auth
        }


@router.get('/')
async def get_auth(name: str, db: Session = Depends(get_db)):
    auth = await read_authorization(name, db)
    return {
        'success': True,
        'authorization': auth
    } if auth is not None else JSONResponse(content={
        'success': False,
        'message': 'No such authorization.'
    }, status_code=404)


@router.get('/all')
async def get_all_auth(db: Session = Depends(get_db)):
    auths = await read_authorizations(db)
    return {
        'success': True,
        'authorizations': auths
    } if len(auths) != 0 else JSONResponse(content={
        'success': False,
        'message': 'No authorizations.'
    }, status_code=404)


@router.patch('/')
async def update_auth(old_name: str = Query(max_length=25),
                      new_name: str = Query(max_length=25),
                      db: Session = Depends(get_db)):
    auth = await update_authorization(old_name=old_name, new_name=new_name, db=db)
    return {
        'success': True,
        'message': 'Successfully changed.'
    } if auth != 0 else JSONResponse(content={
        'success': False,
        'message': 'No such authorization.'
    }, status_code=404)


@router.delete('/')
async def delete_auth(name: str,
                      db: Session = Depends(get_db)):
    rows = await delete_authorization(name, db)
    return {
        'success': True,
        'count': rows
    } if rows != 0 else JSONResponse(content={
        'success': False,
        'message': 'No such authorization.'
    }, status_code=404)
