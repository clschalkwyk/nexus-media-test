from typing import Optional,List
from typing_extensions import TypedDict
from pydantic import BaseModel, Json

class AccountReq(BaseModel):
    email: str
    password: str

class UserProfile(TypedDict, total=False):
    likes: Optional[List[str]]
    dislikes: Optional[List[str]]


class DynamoBaseModel(BaseModel):
    pk: Optional[str]
    sk: Optional[str]

class LocationBasic(BaseModel):
    country: str
    region: str
    city: str
    lat: Optional[str]
    lon: Optional[str]

class ProfileReq(DynamoBaseModel):
    username: str
    profile_image: str
    active: int
    profile: UserProfile
    location: Optional[LocationBasic]
