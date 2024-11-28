# main.py
from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
# 서비스 생성을 위해 필요한 모듈 임포트
from common.FastapiCm import BaseService, BaseDBModel, BaseSchema
from models.UserModel import User, UserCreate, UserUpdate

# 데이터베이스 설정
engine = create_engine("postgresql://user:password@localhost/dbname")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 애플리케이션 생성
app = FastAPI(
    title="User Management API",
    description="User management system"
)

# 데이터베이스 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용자 서비스 생성
user_service = BaseService[User, UserCreate, UserUpdate](User, get_db)

# 라우터 생성 및 등록
security_service = SecurityService(AppConfig())

user_router = APIRouter(
    service=user_service,
    security_service=security_service,
    prefix="/users",
    tags=["users"]
)
user_router.register(app)

# 데이터베이스 의존성
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
