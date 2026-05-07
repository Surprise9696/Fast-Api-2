from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.base import BaseRepository

class LocationRepository(BaseRepository[Location]):
    
    def __init__(self, db: Session):
        super().__init__(db, Location)
    
    def get_published(self, skip: int = 0, limit: int = 100) -> List[Location]:
        return self.db.query(self.model).filter(
            self.model.is_published == True
        ).offset(skip).limit(limit).all()
    
    def get_by_name(self, name: str) -> Optional[Location]:
        return self.db.query(self.model).filter(self.model.name == name).first()