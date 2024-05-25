import datetime
import uuid
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    password_confirm: str


class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str
