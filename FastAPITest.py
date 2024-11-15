# main.py
from fastapi import Depends
from sqlalchemy.orm import Session

# 데이터베이스 설정
# db = Database("postgresql://user:password@localhost/dbname")
# MongoDB 확인
db = Database("postgresql://user:password@localhost/dbname")

# 애플리케이션 생성
app = AppFactory.create_app(
    title="User Management API",
    description="User management system"
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
