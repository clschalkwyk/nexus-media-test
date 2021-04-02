import uvicorn

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
def home():
    return {"Hello"}


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)