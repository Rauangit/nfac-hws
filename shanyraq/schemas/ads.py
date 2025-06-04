from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AdBaseSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, description="Заголовок объявления")
    description: str = Field(..., min_length=40, max_length=1000, description="Описание объявления")
    price: int = Field(..., ge=100, description="Стоимость объявления")
    image_url: str = Field(..., min_length=3, max_length=150, description="URL изображения объявления")


class AdCreateSchema(AdBaseSchema):
    pass


class AdUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50, description="Заголовок объявления")
    description: Optional[str] = Field(None, min_length=20, max_length=1000, description="Описание объявления")
    price: Optional[int] = Field(None, ge=100, le=1_000_000_000, description="Стоимость объявления")
    image_url: Optional[str] = Field(None, min_length=3, max_length=150, description="URL изображения объявления")


class AdReadSchema(AdBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
