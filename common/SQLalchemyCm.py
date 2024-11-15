from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator, Any, List, Dict, Optional, Type
import logging
from datetime import datetime

Base = declarative_base()

class DatabaseManager:
    def __init__(self, connection_string: str, echo: bool = False):
        self.engine = create_engine(connection_string, echo=echo)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        self.logger = logging.getLogger(__name__)

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Session error: {str(e)}")
            raise
        finally:
            session.close()

    #def add_item(self, item: Base) -> Optional[Base]:
    def add_item(self, item: Any) -> Optional[Any]:
        try:
            with self.get_session() as session:
                session.add(item)
                session.flush()
                session.refresh(item)
                return item
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to add item: {str(e)}")
            raise

    #def add_items(self, items: List[Base]) -> List[Base]:
    def add_items(self, items: List[Any]) -> List[Any]:
        try:
            with self.get_session() as session:
                session.add_all(items)
                session.flush()
                for item in items:
                    session.refresh(item)
                return items
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to add items in bulk: {str(e)}")
            raise

    #def get_by_id(self, model: Type[Base], id: Any) -> Optional[Base]:
    def get_by_id(self, model: Type[Any], id: Any) -> Optional[Any]:
        try:
            with self.get_session() as session:
                return session.query(model).filter(model.id == id).first()
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to retrieve item: {str(e)}")
            raise

    # Other methods omitted for brevity