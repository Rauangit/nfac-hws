from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=5, max_length=50)
    full_name: str = Field(..., min_length=5, max_length=50)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=30)


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=5, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=30)
    full_name: Optional[str] = Field(None, min_length=5, max_length=50)


class UserReadSchema(UserBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
