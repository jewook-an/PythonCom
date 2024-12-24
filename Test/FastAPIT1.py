from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, WebSocket
from typing import List
from strawberry.fastapi import GraphQLRouter
import strawberry

app = FastAPI()

###########################################################################
# 파일 업로드
###########################################################################
@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    # 단일 파일 업로드
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

@app.post("/multiple-files/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    # 다중 파일 업로드
    return {"file_names": [file.filename for file in files]}
###########################################################################
# GraphQL 스키마 정의
###########################################################################
@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str) -> str:
        return f"Hello, {name}!"

# GraphQL 라우터 생성
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# FastAPI 앱에 GraphQL 라우터 추가
app.include_router(graphql_app, prefix="/graphql")


###########################################################################
# 데이터 베이스
###########################################################################
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import os

# 데이터베이스 모델 정의
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


# 데이터베이스 세션 생성
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:

    # 데이터베이스 의존성 함수
    def get_db():
        db = SessionLocal()
        try:
            # https://www.daleseo.com/python-yield/
            # yield 키워드 사용시 제너레이터 반환 : return > 모든 값 메모리에 올림, yield > 결과 값을 하나씩 메모리에 올림.
            # 메모리에 한번에 올리기 부담스러운 대용량 파일 Read, 스트림 데이터 처리시 유용.
            yield db
        finally:
            db.close()
    # yield 사용예
    def yield_abc1():
        for ch in ["A", "B", "C"]:
            yield ch
    # yield from 사용시 리스트를 바로 제너레이터로 변환 : 매우편리함
    def yield_abc2():
        yield from ["A", "B", "C"]

    # 사용자 생성 엔드포인트
    @app.post("/users/")
    def create_user(name: str, email: str, db: Session = Depends(get_db)):
        new_user = User(name=name, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


###########################################################################
# 인증 및 보안
###########################################################################
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

# OAuth2 인증 스키마
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 비밀 키와 알고리즘 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# 토큰 검증 함수
def verify_token(token: str):
    try:
        # 토큰 디코딩 로직
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# 보호된 엔드포인트
@app.get("/protected-route")
async def protected_route(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return {"message": "Access granted", "user": user}


###########################################################################
# WebSocket 통신
###########################################################################
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 메시지 수신
            data = await websocket.receive_text()
            # 메시지 송신
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        await websocket.close()

# 서버 코드 (FastAPI 웹소켓)
import asyncio
import random
app = FastAPI()

@app.websocket("/ws/stocks")
async def stock_price_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 주식 가격을 임의로 생성
            stock_price = random.uniform(100, 500)
            # 주식 가격을 클라이언트에 전송
            await websocket.send_text(f"Stock Price: ${stock_price:.2f}")
            # 1초 대기
            await asyncio.sleep(1)
    except Exception as e:
        await websocket.close()