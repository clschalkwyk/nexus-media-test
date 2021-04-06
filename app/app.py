import uvicorn
import boto3
import jwt
import datetime
import os
import json
import shutil
from boto3.dynamodb.conditions import Key
from hashlib import sha256
from uuid import uuid4
from fastapi import FastAPI, Header, Depends, UploadFile, File
from typing import Optional
from mangum import Mangum

from .models import account
from .models.config import Settings
from .libs.auth import authorized, get_user

config = Settings()
dy_table = config.DYNAMO_TABLE
jwt_secret = config.JWT_SECRET
jwt_exp = config.JWT_EXP
pwd_salt = config.PWD_SALT

app = FastAPI()


@app.get("/")
def home():
    return {"Hello 4"}


# auth
@app.post("/auth")
def auth_join(account: account.AccountReq):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(dy_table)
    domain = 'cyberstaffing'
    sk = 'ACC#{}#{}'.format(domain, account.email)

    resp = table.query(
        KeyConditionExpression=Key('sk').eq(sk),
        IndexName='reverseIndexIdx'
    )

    if resp.get('Count') == 0:
        h = sha256()
        h.update("{}".format(account.password).encode('utf8'))
        salt = h.hexdigest()
        h.update("{}:{}:{}".format(account.password, salt, pwd_salt).encode('utf8'))
        hash = h.hexdigest()

        acc = {
            'pk': uuid4().__str__(),
            'sk': sk,
            'domain': domain,
            'email': account.email,
            'password': hash
        }

        table.put_item(Item=acc)
        return {"result": 200, "message": "Welcome {} {}".format(account.email, account.password)}

    return {"result": 500, "message": "error"}


@app.post("/auth/login")
def auth_login(account: account.AccountReq):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(dy_table)
    domain = 'cyberstaffing'
    sk = 'ACC#{}#{}'.format(domain, account.email)

    resp = table.query(
        KeyConditionExpression=Key('sk').eq(sk),
        IndexName='reverseIndexIdx'
    )

    if resp.get('Count') == 1:
        h = sha256()
        h.update("{}".format(account.password).encode('utf8'))
        salt = h.hexdigest()
        h.update("{}:{}:{}".format(account.password, salt, pwd_salt).encode('utf8'))
        hash = h.hexdigest()

        if resp['Items'][0]['password'] == hash:
            payload = {
                "email": account.email,
                "domain": domain,
                "userId": resp['Items'][0]['pk'],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=jwt_exp)
            }
            print(payload)
            encoded = jwt.encode(payload, jwt_secret, algorithm='HS256')
            return {"result": 200, "token": encoded}

    return {"result": 500, "message": "Authentication failed."}


@app.get("/auth/me")
def auth_me(authorization: Optional[str] = Header(None)):
    try:
        jtoken = authorization.split('Bearer')[1].strip()
        decoded = jwt.decode(jtoken, jwt_secret, algorithms='HS256')
        return {"me": decoded}
    except jwt.exceptions.ExpiredSignatureError:
        return {"error": "Session expired."}



@app.get("/auth/test", dependencies=[Depends(authorized)])
def auth_test():
    return {"me": "yes"}

# profile
@app.post('/account/profile')
def account_profile(profile: account.ProfileReq, user: dict = Depends(get_user)):
    print(profile.json())
    print(user.get('userId'))

    return {"profile"}


@app.post('/account/media')
def account_media(image: UploadFile = File(...), user: dict = Depends(get_user)):
    print(user)
    print(image)

    temp_filename = '{}{}'.format(uuid4().__str__(), os.path.splitext(image.filename)[1])
    print(temp_filename)
    with open('uploads/{}'.format(temp_filename), 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    # check file exists
    # upoload to S3
    # write media gallery
    return {'uploaded': image.filename, "temp": temp_filename}





# content
# media
# catalog

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
