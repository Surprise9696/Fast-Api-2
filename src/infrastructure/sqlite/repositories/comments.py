from typing import List
from sqlalchemy.orm import Session, joinedload
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.repositories.base import BaseRepository

class CommentRepository(BaseRepository[Comment]):
    
    def __init__(self, db: Session):
        super().__init__(db, Comment)
    
    def get_by_post(self, post_id: int) -> List[Comment]:
        return self.db.query(self.model).filter(
            self.model.post_id == post_id
        ).options(
            joinedload(self.model.author)
        ).order_by(self.model.created_at.desc()).all()
    
    def get_by_author(self, author_id: int) -> List[Comment]:
        return self.db.query(self.model).filter(
            self.model.author_id == author_id
        ).options(
            joinedload(self.model.post)
        ).order_by(self.model.created_at.desc()).all()
    
    def get_recent(self, limit: int = 10) -> List[Comment]:
        return self.db.query(self.model).options(
            joinedload(self.model.author),
            joinedload(self.model.post)
        ).order_by(self.model.created_at.desc()).limit(limit).all()