from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    photo: Optional[str] = None

class FlowerCreate(BaseModel):
    name: str
    quantity: int
    price: float

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
