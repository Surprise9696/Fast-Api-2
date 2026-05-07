from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.repositories.base import BaseRepository

class PostRepository(BaseRepository[Post]):
    
    def __init__(self, db: Session):
        super().__init__(db, Post)
    
    def get_by_id_with_relations(self, id: int) -> Optional[Post]:
        return self.db.query(self.model).options(
            joinedload(self.model.author),
            joinedload(self.model.category),
            joinedload(self.model.location)
        ).filter(self.model.id == id).first()
    
    def get_published(
        self, 
        skip: int = 0, 
        limit: int = 10,
        category_id: Optional[int] = None,
        location_id: Optional[int] = None
    ) -> List[Post]:
        query = self.db.query(self.model).filter(
            self.model.is_published == True,
            self.model.pub_date <= datetime.now()
        )
        
        if category_id:
            query = query.filter(self.model.category_id == category_id)
        
        if location_id:
            query = query.filter(self.model.location_id == location_id)
        
        return query.order_by(self.model.pub_date.desc()).offset(skip).limit(limit).all()
    
    def get_by_author(self, author_id: int) -> List[Post]:
        return self.db.query(self.model).filter(
            self.model.author_id == author_id
        ).options(
            joinedload(self.model.category),
            joinedload(self.model.location)
        ).all()
    
    def get_by_category(self, category_id: int) -> List[Post]:
        return self.db.query(self.model).filter(
            self.model.category_id == category_id,
            self.model.is_published == True,
            self.model.pub_date <= datetime.now()
        ).options(
            joinedload(self.model.author)
        ).order_by(self.model.pub_date.desc()).all()
    
    def search(self, search_term: str) -> List[Post]:
        return self.db.query(self.model).filter(
            self.model.is_published == True,
            self.model.pub_date <= datetime.now()
        ).filter(
            (self.model.title.contains(search_term)) |
            (self.model.text.contains(search_term))
        ).options(
            joinedload(self.model.author),
            joinedload(self.model.category)
        ).order_by(self.model.pub_date.desc()).all()