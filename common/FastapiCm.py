from fastapi import FastAPI, HTTPException, Depends, Security, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
import jwt
import logging
from contextlib import contextmanager
import time

# 제네릭 타입 변수 정의
T = TypeVar("T")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class AppConfig:
    """애플리케이션 설정"""
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
class PageResponse(BaseModel, Generic[T]):
    """페이지네이션 응답 모델"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class TokenResponse(BaseModel):
    """토큰 응답 모델"""
    access_token: str
    token_type: str
    
class BaseAPIRouter:
    """기본 API 라우터"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """요청 로깅 미들웨어"""
    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        log_dict = {
            "path": request.url.path,
            "method": request.method,
            "process_time": f"{process_time:.2f}s",
            "status_code": response.status_code
        }
        logging.info(f"Request processed: {log_dict}")
        
        return response

class BaseService(Generic[T, CreateSchemaType, UpdateSchemaType]):
    """기본 서비스 클래스"""
    def __init__(self, model: T):
        self.model = model

    async def create(self, db: Session, schema: CreateSchemaType) -> T:
        db_item = self.model(**schema.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    async def get_by_id(self, db: Session, id: int) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_all(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> PageResponse[T]:
        total = db.query(self.model).count()
        items = db.query(self.model).offset(skip).limit(limit).all()
        return PageResponse(
            items=items,
            total=total,
            page=(skip // limit) + 1,
            size=limit,
            pages=(total + limit - 1) // limit
        )

    async def update(
        self, 
        db: Session, 
        id: int, 
        schema: UpdateSchemaType
    ) -> Optional[T]:
        db_item = await self.get_by_id(db, id)
        if db_item:
            for key, value in schema.dict(exclude_unset=True).items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
        return db_item

    async def delete(self, db: Session, id: int) -> bool:
        db_item = await self.get_by_id(db, id)
        if db_item:
            db.delete(db_item)
            db.commit()
            return True
        return False

class APIExceptionHandler:
    """API 예외 처리 핸들러"""
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @staticmethod
    async def validation_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc)}
        )

class SecurityService:
    """보안 서비스"""
    def __init__(self, config: AppConfig):
        self.config = config
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, 
            self.config.SECRET_KEY, 
            algorithm=self.config.ALGORITHM
        )

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, 
                self.config.SECRET_KEY, 
                algorithms=[self.config.ALGORITHM]
            )
            return payload
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

class APIRouter(BaseAPIRouter):
    """API 라우터"""
    def __init__(
        self, 
        service: BaseService,
        security_service: Optional[SecurityService] = None,
        prefix: str = "",
        tags: List[str] = None
    ):
        super().__init__()
        self.service = service
        self.security_service = security_service
        self.prefix = prefix
        self.tags = tags or []

    def register(self, app: FastAPI):
        """라우트 등록"""
        
        @app.post(
            f"{self.prefix}/",
            response_model=self.service.model,
            tags=self.tags
        )
        async def create(
            item: CreateSchemaType,
            db: Session = Depends(get_db),
            token: str = Depends(self.security_service.oauth2_scheme)
            if self.security_service else None
        ):
            return await self.service.create(db, item)

        @app.get(
            f"{self.prefix}/{{id}}",
            response_model=self.service.model,
            tags=self.tags
        )
        async def get_by_id(
            id: int,
            db: Session = Depends(get_db)
        ):
            item = await self.service.get_by_id(db, id)
            if not item:
                raise HTTPException(
                    status_code=404,
                    detail="Item not found"
                )
            return item

        @app.get(
            f"{self.prefix}/",
            response_model=PageResponse[self.service.model],
            tags=self.tags
        )
        async def get_all(
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db)
        ):
            return await self.service.get_all(db, skip, limit)

        @app.put(
            f"{self.prefix}/{{id}}",
            response_model=self.service.model,
            tags=self.tags
        )
        async def update(
            id: int,
            item: UpdateSchemaType,
            db: Session = Depends(get_db),
            token: str = Depends(self.security_service.oauth2_scheme)
            if self.security_service else None
        ):
            updated_item = await self.service.update(db, id, item)
            if not updated_item:
                raise HTTPException(
                    status_code=404,
                    detail="Item not found"
                )
            return updated_item

        @app.delete(
            f"{self.prefix}/{{id}}",
            tags=self.tags
        )
        async def delete(
            id: int,
            db: Session = Depends(get_db),
            token: str = Depends(self.security_service.oauth2_scheme)
            if self.security_service else None
        ):
            if not await self.service.delete(db, id):
                raise HTTPException(
                    status_code=404,
                    detail="Item not found"
                )
            return {"status": "success"}

class AppFactory:
    """애플리케이션 팩토리"""
    @staticmethod
    def create_app(
        title: str = "FastAPI App",
        description: str = "FastAPI application with common features",
        version: str = "1.0.0",
        config: AppConfig = AppConfig()
    ) -> FastAPI:
        app = FastAPI(title=title, description=description, version=version)
        
        # CORS 미들웨어 추가
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 로깅 미들웨어 추가
        app.middleware("http")(RequestLoggingMiddleware())
        
        # 예외 핸들러 등록
        app.add_exception_handler(
            HTTPException,
            APIExceptionHandler.http_exception_handler
        )
        app.add_exception_handler(
            Exception,
            APIExceptionHandler.validation_exception_handler
        )
        
        return app

# 예시 스키마 및 사용법
class UserBase(BaseModel):
    """기본 사용자 스키마"""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """사용자 생성 스키마"""
    password: str

class UserUpdate(BaseModel):
    """사용자 업데이트 스키마"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    """사용자 응답 스키마"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# 사용 예시
"""
# main.py
from fastapi import Depends
from sqlalchemy.orm import Session

# 데이터베이스 설정
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
"""
