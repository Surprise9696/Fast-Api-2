from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BaseModelSchema(BaseModel):
    is_published: bool = Field(
        True, 
        description="Опубликовано. Снимите галочку, чтобы скрыть публикацию."
    )
    created_at: datetime = Field(default_factory=datetime.now)

class Location(BaseModelSchema):
    id: Optional[int] = None
    name: str = Field(max_length=256)


class LocationCreate(BaseModelSchema):
    name: str = Field(max_length=256)


class LocationUpdate(BaseModelSchema):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None
