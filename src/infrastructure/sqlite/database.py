from contextlib import contextmanager
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        base_dir = Path(__file__).parent.parent.parent.parent.parent
        db_path = base_dir / "db.sqlite3"
        self._db_url = f"sqlite:///{db_path}"
        
        self._engine = create_engine(
            self._db_url,
            connect_args={"check_same_thread": False}
        )

        self._SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    @contextmanager
    def session(self):
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


database = Database()
Base = declarative_base()