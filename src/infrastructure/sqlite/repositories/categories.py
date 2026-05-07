from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.base import BaseRepository

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(db, Category)
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.db.query(self.model).filter(self.model.slug == slug).first()
    
    def get_published(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.db.query(self.model).filter(
            self.model.is_published == True
        ).offset(skip).limit(limit).all()
    
    def search_by_title(self, title: str) -> List[Category]:
        return self.db.query(self.model).filter(
            self.model.title.contains(title)
        ).all()