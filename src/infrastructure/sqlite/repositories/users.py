from typing import Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.users import User
from src.infrastructure.sqlite.repositories.base import BaseRepository
from datetime import datetime

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def create(self, **kwargs) -> User:
        if 'is_superuser' not in kwargs:
            kwargs['is_superuser'] = False
        if 'is_staff' not in kwargs:
            kwargs['is_staff'] = False
        if 'is_active' not in kwargs:
            kwargs['is_active'] = True
        if 'date_joined' not in kwargs:
            kwargs['date_joined'] = datetime.now()
            
        return super().create(**kwargs)
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.email == email).first()