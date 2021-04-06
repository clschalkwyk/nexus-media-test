import jwt
from fastapi import Header
from typing import Optional

from app.models.config import Settings

config = Settings()

jwt_secret = config.JWT_SECRET


async def authorized(authorization: Optional[str] = Header(None)):
    try:
        if authorization:
            jtoken = authorization.split('Bearer')[1].strip()
            decoded = jwt.decode(jtoken, jwt_secret, algorithms='HS256')
            print(decoded)
        else:
            raise Exception("Error")
    except jwt.exceptions.ExpiredSignatureError:
        raise Exception("Error")
    except:
        raise Exception("Error")

async def get_user(authorization: Optional[str] = Header(None)):
    try:
        jtoken = authorization.split('Bearer')[1].strip()
        decoded = jwt.decode(jtoken, jwt_secret, algorithms='HS256')
        return decoded
    except jwt.exceptions.ExpiredSignatureError:
        return {"error": "Session expired."}