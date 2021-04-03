import uvicorn
import boto3
from hashlib import sha256
from uuid import uuid4
from pydantic import BaseModel
from fastapi import FastAPI
from mangum import Mangum


class JoinReq(BaseModel):
    email: str
    password: str


dy_table = ''


app = FastAPI()

@app.get("/")
def home():
    return {"Hello 4"}


# auth
@app.post("/auth")
def auth_join(account: JoinReq):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(dy_table)

    h = sha256()
    h.update("{}".format(account.password).encode('utf8'))
    hash = h.hexdigest()
    acc = {
        'pk': uuid4().__str__(),
        'sk': 'ACC',
        'domain': 'cyberstaffing',
        'email' : account.email,
        'password': hash
    }

    res = table.put_item(Item=acc)

    print(res)
    return {"message": "Welcome {} {}".format(account.email, account.password)}


# content
# media
# catalog

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
