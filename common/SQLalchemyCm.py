from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator, Any, List, Dict, Optional, Type
import logging
from datetime import datetime

# Base 클래스 생성
Base = declarative_base()

class DatabaseManager:
    """
    SQLAlchemy를 사용한 데이터베이스 관리 클래스
    """

    def __init__(self, connection_string: str, echo: bool = False):
        """
        DatabaseManager 초기화

        Args:
            connection_string (str): 데이터베이스 연결 문자열
            echo (bool): SQL 쿼리 로깅 여부
        """
        self.engine = create_engine(connection_string, echo=echo)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        self.logger = logging.getLogger(__name__)

    def create_tables(self) -> None:
        """
        모든 정의된 테이블 생성
        """
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        데이터베이스 세션 컨텍스트 매니저
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"세션 에러: {str(e)}")
            raise
        finally:
            session.close()

    def add_item(self, item: Any) -> Optional[Any]:
        """
        단일 아이템 추가
        """
        try:
            with self.get_session() as session:
                session.add(item)
                session.flush()
                session.refresh(item)
                return item
        except SQLAlchemyError as e:
            self.logger.error(f"아이템 추가 실패: {str(e)}")
            raise

    def add_items(self, items: List[Any]) -> List[Any]:
        """
        여러 아이템 일괄 추가
        """
        try:
            with self.get_session() as session:
                session.add_all(items)
                session.flush()
                for item in items:
                    session.refresh(item)
                return items
        except SQLAlchemyError as e:
            self.logger.error(f"아이템 일괄 추가 실패: {str(e)}")
            raise

    def get_by_id(self, model: Any, id: Any) -> Optional[Any]:
        """
        ID로 단일 아이템 조회
        """
        try:
            with self.get_session() as session:
                return session.query(model).filter(model.id == id).first()
        except SQLAlchemyError as e:
            self.logger.error(f"아이템 조회 실패: {str(e)}")
            raise

    def get_all(self, model: Any, skip: int = 0, limit: int = 100) -> List[Any]:
        """
        모든 아이템 조회 (페이지네이션 지원)
        """
        try:
            with self.get_session() as session:
                return session.query(model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            self.logger.error(f"전체 조회 실패: {str(e)}")
            raise

    def update_item(self, model: Any, id: Any, update_data: Dict[str, Any]) -> Optional[Any]:
        """
        아이템 업데이트
        """
        try:
            with self.get_session() as session:
                item = session.query(model).filter(model.id == id).first()
                if item:
                    for key, value in update_data.items():
                        if hasattr(item, key):
                            setattr(item, key, value)
                    session.flush()
                    session.refresh(item)
                return item
        except SQLAlchemyError as e:
            self.logger.error(f"아이템 업데이트 실패: {str(e)}")
            raise

    def delete_item(self, model: Any, id: Any) -> bool:
        """
        아이템 삭제
        """
        try:
            with self.get_session() as session:
                item = session.query(model).filter(model.id == id).first()
                if item:
                    session.delete(item)
                    return True
                return False
        except SQLAlchemyError as e:
            self.logger.error(f"아이템 삭제 실패: {str(e)}")
            raise

    def execute_raw_query(self, query: str, params: Optional[Dict] = None) -> List[Any]:
        """
        Raw SQL 쿼리 실행
        """
        try:
            with self.get_session() as session:
                result = session.execute(text(query), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            self.logger.error(f"쿼리 실행 실패: {str(e)}")
            raise

    def bulk_insert(self, model: Any, items: List[Dict[str, Any]]) -> None:
        """
        대량 데이터 삽입
        """
        try:
            with self.get_session() as session:
                session.bulk_insert_mappings(model, items)
        except SQLAlchemyError as e:
            self.logger.error(f"대량 삽입 실패: {str(e)}")
            raise

    def get_by_filter(self, model: Any, filters: Dict[str, Any]) -> List[Any]:
        """
        필터 조건으로 아이템 조회
        """
        try:
            with self.get_session() as session:
                query = session.query(model)
                for key, value in filters.items():
                    if hasattr(model, key):
                        query = query.filter(getattr(model, key) == value)
                return query.all()
        except SQLAlchemyError as e:
            self.logger.error(f"필터 조회 실패: {str(e)}")
            raise

# 예시 모델 클래스
class User(Base):
    """예시: User 모델"""
    __tablename__ = "users"

    from sqlalchemy import Column, Integer, String, DateTime

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)