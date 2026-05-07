from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .users import User

class Comment(BaseModel):
    id: Optional[int] = None
    post_id: int
    author: User
    text: str
    created_at: datetime = Field(default_factory=datetime.now)


class CommentCreate(BaseModel):
    post_id: int
    author_id: int
    text: str


class CommentUpdate(BaseModel):
    text: Optional[str] = None

