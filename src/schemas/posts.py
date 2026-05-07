from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.schemas.users import User
from src.schemas.category import Category
from src.schemas.location import Location


class BaseModelSchema(BaseModel):
    is_published: bool = Field(
        True,
        description="Опубликовано. Снимите галочку, чтобы скрыть публикацию."
    )
    created_at: datetime = Field(default_factory=datetime.now)


class Post(BaseModelSchema):
    id: Optional[int] = None
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime = Field(
        description="Если установить дату и время в будущем — можно делать отложенные публикации."
    )
    author: User
    location: Optional[Location] = None
    category: Category
    image: Optional[str] = Field(None, description="URL изображения")

    @property
    def is_past_pub_date(self) -> bool:
        return self.pub_date <= datetime.now(self.pub_date.tzinfo)


class PostCreate(BaseModelSchema):
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: int
    image: Optional[str] = None
    is_published: bool = True


class PostUpdate(BaseModelSchema):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: Optional[bool] = None


class PostListResponse(BaseModel):
    id: int
    title: str
    text: str
    pub_date: datetime
    author_id: int
    category_id: int
    image: Optional[str] = None
