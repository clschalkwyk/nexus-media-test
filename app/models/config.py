from pydantic import BaseSettings

class Settings(BaseSettings):
    DYNAMO_TABLE: str
    JWT_SECRET: str
    JWT_EXP: int
    PWD_SALT: str

    class Config:
        env_file = '.env'