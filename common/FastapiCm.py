from fastapi import FastAPI, HTTPException, Depends, Security, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from typing import Generic, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
import jwt
import logging
from contextlib import contextmanager
import time

# Base 클래스 생성
Base = declarative_base()

# 제네릭 타입 변수 정의
T = TypeVar("T")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

# Database 설정 클래스 추가
class DatabaseConfig:
    """데이터베이스 설정"""
    def __init__(
        self,
        # db_url: str = "sqlite:///./test.db",
        db_url: str = "postgresql://postgres:godlast@localhost:5432/postgres",
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30
    ):
        self.db_url = db_url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout

class Database:
    """데이터베이스 관리 클래스"""
    def __init__(self, config: DatabaseConfig):
        self.engine = create_engine(
            config.db_url,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_timeout=config.pool_timeout
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        self.Base = declarative_base()

    def create_tables(self):
        """데이터베이스 테이블 생성"""
        self.Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_db(self):
        """데이터베이스 세션 컨텍스트 매니저"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_db_dependency(self):
        """FastAPI 의존성으로 사용할 데이터베이스 세션 제공자"""
        def _get_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()
        return _get_db

class AppConfig:
    """애플리케이션 설정"""
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# [이전 코드와 동일한 부분...]
# PageResponse, TokenResponse, BaseAPIRouter, RequestLoggingMiddleware 등은 그대로 유지

# HTTPException 핸들러 정의(2024-12-20 Cursor 추가)
async def http_exception_handler(request: Request, exc: HTTPException):
   return JSONResponse(
       status_code=exc.status_code,
       content={"detail": exc.detail},
   )

class AppFactory:
    """애플리케이션 팩토리"""
    @staticmethod
    def create_app(
        title: str = "FastAPI App",
        description: str = "FastAPI application with common features",
        version: str = "1.0.0",
        config: AppConfig = AppConfig(),
        db_config: DatabaseConfig = DatabaseConfig()
    ) -> tuple[FastAPI, Database]:
        app = FastAPI(title=title, description=description, version=version)

        # 데이터베이스 초기화
        db = Database(db_config)
        db.create_tables()

        # CORS 미들웨어 추가
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 로깅 미들웨어 추가
        #app.middleware("http")(RequestLoggingMiddleware())
        # 예외 핸들러 등록 (2024-12-20 Cursor 수정)
        app.add_exception_handler(HTTPException, http_exception_handler)  # 핸들러 추가
        # 필요시 추가
        #app.add_exception_handler(Exception, some_other_handler)  # 다른 핸들러도 추가 가능
        """
        # 예외 핸들러 등��� (Error )
        app.add_exception_handler(
            HTTPException,
            # APIExceptionHandler.http_exception_handler
        )
        app.add_exception_handler(
            Exception,
            # APIExceptionHandler.validation_exception_handler
        )
        """

        return app, db

# 기본 모델 클래스들 추가
class BaseDBModel(Base):
    """기본 데이터베이스 모델"""
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

class BaseSchema(BaseModel):
    """기본 Pydantic 스키마"""
    class Config:
        from_attributes = True

# 사용 예시:
"""
# main.py
from fastapi import Depends
from sqlalchemy.orm import Session

# 애플리케이션 및 데이터베이스 생성
app, db = AppFactory.create_app(
    title="User Management API",
    description="User management system",
    db_config=DatabaseConfig(db_url="postgresql://user:password@localhost/dbname")
)

# 서비스 생성
user_service = BaseService[User, UserCreate, UserUpdate](User)

# 라우터 생성 및 등록
security_service = SecurityService(AppConfig())
user_router = APIRouter(
    service=user_service,
    security_service=security_service,
    prefix="/users",
    tags=["users"]
)

# 데이터베이스 의존성 설정
get_db = db.get_db_dependency()

# 라우터 등록 (get_db 의존성이 설정된 후)
user_router.register(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""