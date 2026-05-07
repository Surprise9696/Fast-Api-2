from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Iterator
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories import (
    UserRepository,
    CategoryRepository,
    LocationRepository,
    PostRepository,
    CommentRepository
)

def get_db() -> Iterator[Session]:
    with database.session() as session:
        yield session

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)

def get_location_repository(db: Session = Depends(get_db)) -> LocationRepository:
    return LocationRepository(db)

def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(db)

def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepository:
    return CommentRepository(db)