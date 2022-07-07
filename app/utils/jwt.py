from datetime import datetime, timedelta, timezone

from jwt import encode, decode


def issue_token(user_info: dict, delta: timedelta):
    """
    This function doesn't take care of errors!

    :param user_info:
    :param delta:
    :return:
    """
    payload = user_info.copy()

    payload.update({'iat': datetime.now(tz=timezone.utc), 'exp': datetime.now(tz=timezone.utc) + delta})

    jwt = encode(payload=payload, key='secret_key', algorithm='HS256')

    return jwt


def extract_payload_from_token(token: str):
    """
    This function doesn't take care of errors!

    :param token:
    :return:
    """
    payload = decode(jwt=token, key='secret_key', algorithms=['HS256'])

    return payload
