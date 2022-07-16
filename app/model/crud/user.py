import uuid

from sqlalchemy.orm import Session

from .. import models

"""
This functions are not capable to authentication every actions.
"""


async def create_user(db: Session,
                      github_id: str,
                      email: str,
                      name: str,
                      thumbnail_url: str | None = None,
                      authorization_name: str = 'member',
                      refresh_token: str | None = None) -> models.User:
    """
    Create user into database.

    :param thumbnail_url: Thumbnail image url from GitHub user info.
    :param github_id: GitHub id provided by GitHub.
    :param email: email address.
    :param name: full name.
    :param authorization_name: name which is in `Authorization` in database.
    :param refresh_token: Refresh token.
    :param db:
    :return:
    """
    user = models.User(uuid=str(uuid.uuid4()),
                       github_id=github_id,
                       email=email,
                       name=name,
                       authorization=authorization_name,
                       thumbnail_url=thumbnail_url,
                       refresh_token=refresh_token)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def read_user(db: Session,
                    user_id: str) -> models.User:
    """
    Return user data using one of parameter below.
    """
    return db.query(models.User.user_id,
                    models.User.email,
                    models.User.name,
                    models.User.authorization,
                    models.User.created_at,
                    models.User.thumbnail_url) \
        .filter(models.User.user_id == user_id).first()


async def read_users(db: Session) -> [models.User]:
    return db.query(models.User.user_id,
                    models.User.email,
                    models.User.name,
                    models.User.authorization,
                    models.User.created_at,
                    models.User.thumbnail_url).all()


async def update_user(db: Session,
                      user_id: str,
                      email: str,
                      name: str,
                      thumbnail_url: str | None = None,
                      refresh_token: str | None = None,
                      authorization_name: str = 'member') -> models.User:
    """
    Identify user only with **user_id**!!!
    Check authorization first!!!

    :param authorization_name: Check GET `/authorization/all` first.
    :param thumbnail_url: Thumbnail image url from GitHub user info you want to fix.
    :param user_id: Using when identifying user.
    :param email: Field to update.
    :param name: Field to update.
    :param refresh_token: Field to update. Not required.
    :param authrization_name: Field to update. Not required.
    :param db:
    :return:
    """

    user = db \
        .query(models.User) \
        .filter(models.User.user_id == user_id) \
        .update({'email': email,
                 'name': name,
                 'authorization': authorization_name,
                 'refresh_token': refresh_token,
                 'thumbnail_url': thumbnail_url})
    db.commit()

    return user


async def delete_user(user_id: str, db: Session) -> int:
    """
    Delete user using `user_id`. This function doesn't check authorization.

    :param user_id: Using when identifying user.
    :param db:
    :return:
    """
    rows = db.query(models.User).filter(models.User.user_id == user_id).delete()
    db.commit()
    return rows
