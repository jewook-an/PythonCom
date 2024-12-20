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
# db_manager = DatabaseManager('postgresql://postgres:godlast@localhost/postgres')
engine = create_engine("postgresql://postgres:godlast@localhost/postgres")
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


# from common.SecurityService import SecurityService  # SecurityService 임포트 추가

class SecurityService:          # example 로 신규 생성 필요
    def __init__(self, config):
        self.config = config
    def authenticate(self, user_credentials):
        # 인증 로직 구현
        pass
    def authorize(self, user, permission):
        # 권한 부여 로직 구현
        pass

# AppConfig 샘플 클래스 정의
class SampleAppConfig:
   def __init__(self):
       self.setting1 = "value1"
       self.setting2 = "value2"
       # 필요한 설정 추가

# 라우터 생성 및 등록
app_config = SampleAppConfig()  # 샘플 AppConfig 인스턴스 생성
security_service = SecurityService(config=app_config)  # 샘플 인스턴스를 사용
# security_service = SecurityService(AppConfig())

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
