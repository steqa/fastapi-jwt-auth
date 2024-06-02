import datetime
import re
import uuid
from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    password_confirm: str

    @field_validator('first_name')
    def validate_first_name(cls, first_name: str) -> str:
        if len(first_name.replace(' ', '')) < 1:
            raise ValueError('First Name must be at least 1 characters long')
        return first_name

    @field_validator('last_name')
    def validate_last_name(cls, last_name: str) -> str:
        if len(last_name.replace(' ', '')) < 1:
            raise ValueError('Last Name must be at least 1 characters long')
        return last_name

    @field_validator('password_confirm')
    def validate_password_confirm(cls, password_confirm: str,
                                  info: ValidationInfo) -> str:
        password = info.data.get('password')
        if password and password_confirm != password:
            raise ValueError("Passwords don't match")
        return password_confirm

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        uppercase_regex = re.compile(r'[A-Z]')
        lowercase_regex = re.compile(r'[a-z]')
        digit_regex = re.compile(r'[0-9]')
        special_char_regex = re.compile(r'[!@#$%^&*()_+{}|:<>?~\-=\[\];\',./]')

        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(uppercase_regex, password):
            raise ValueError('Password must have at least one capital letter')
        if not re.search(lowercase_regex, password):
            raise ValueError(
                'Password must have at least one lowercase letter')
        if not re.search(digit_regex, password):
            raise ValueError('Password must have at least one digit')
        if not re.search(special_char_regex, password):
            raise ValueError(
                'Password must have at least one special character')
        return password


class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str