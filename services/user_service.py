from os import environ
from repositories import user_repository
import bcrypt
import jwt
import time


def get(user_id: int):
    return user_repository.get(user_id)


def get_by_username(username: str):
    if not username:
        return 'Username is None', 400

    user = user_repository.get_by_username(username)
    result, code = (user.get_dict(), 200) if user else (user, 404)

    return result, code


def login(data: dict):
    user, code = get_by_username(data['username'])
    if not user:
        return "User not found", 404
    
    encoded_password = user['password']

    if bcrypt.checkpw(data['password'].encode('utf-8'), encoded_password.encode('utf-8')):
        del user['password']
        
        # user['kid'] = environ.get('KEY')
        user['iat'] = round(time.time() * 1000)
        user['exp'] = round(time.time() * 1000) + 7200000 # 2 hours from now
        encoded_jwt = jwt.encode(payload=user, key=environ.get('JWT_SECRET'), algorithm=environ.get('JWT_ALGORITHM'))
        
        return encoded_jwt, 200
