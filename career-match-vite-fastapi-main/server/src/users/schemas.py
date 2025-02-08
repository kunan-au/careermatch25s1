from typing import Optional

from src.models import CustomModel


class UserBase(CustomModel):
    email: str
    name: str
    avatar: str
    resume: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: Optional[str] = None
    name: str
    avatar: str
    resume: str

class UserRead(UserBase):
    pass

    class Config:
        orm_mode = True
