from typing import Optional,List
from typing_extensions import TypedDict
from pydantic import BaseModel, Json

class AccountReq(BaseModel):
    email: str
    password: str

class UserProfile(TypedDict, total=False):
    likes: Optional[List[str]]
    dislikes: Optional[List[str]]

class ProfileReq(BaseModel):
    username: str
    profile_image: str
    active: int
    profile: UserProfile