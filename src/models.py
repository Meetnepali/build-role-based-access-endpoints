from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfileCreate(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None

class UserProfile(UserProfileCreate):
    profile_picture_url: Optional[str] = None
