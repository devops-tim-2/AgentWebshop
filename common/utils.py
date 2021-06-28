from werkzeug import datastructures
from os import environ
from services import user_service
from datetime import datetime
import jwt


def check(obj: dict) -> bool:
    return not obj or any(prop is None or ((type(prop) is list or type(prop) is str) and len(prop) == 0) or ((type(prop) is int or type(prop) is float) and prop < 1) for prop in list(obj.values()))


def auth(headers: datastructures.Headers):
    if not headers.has_key('Authorization'):
        return 'Forbidden, unauthorized atempt.', 403

    token = headers['Authorization'].split(' ')[1]
    try:
        payload = jwt.decode(token, environ.get('JWT_SECRET'), environ.get('JWT_ALGORITHM'))
    except:
        return 'Forbidden, invalid authentication.', 401

    exp = payload['exp']
    if datetime.now() > datetime.fromtimestamp(exp / 1000.0):
        return 'Forbidden, authorization token has expired.', 401

    return user_service.get_by_username(payload['username'])
