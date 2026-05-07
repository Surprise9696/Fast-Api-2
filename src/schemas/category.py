from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BaseModelSchema(BaseModel):
    is_published: bool = Field(
        True, 
        description="Опубликовано. Снимите галочку, чтобы скрыть публикацию."
    )
    created_at: datetime = Field(default_factory=datetime.now)


class Category(BaseModelSchema):
    id: Optional[int] = None
    title: str = Field(max_length=256)
    description: str
    slug: str = Field(
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание."
    )


class CategoryCreate(BaseModelSchema):
    title: str = Field(max_length=256)
    description: str
    slug: str = Field(
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание."
    )


class CategoryUpdate(BaseModelSchema):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = Field(
        None, 
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: Optional[bool] = None
