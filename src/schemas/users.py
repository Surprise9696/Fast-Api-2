from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: str = Field(...)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    is_superuser: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_superuser: bool
    is_staff: bool
    is_active: bool
    last_login: Optional[datetime] = None
    date_joined: Optional[datetime] = None
    
    class Config:
        from_attributes = True