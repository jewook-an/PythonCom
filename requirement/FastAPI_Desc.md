### 목차

1. [FastAPI주요기능](#1-FastAPI-주요기능)
2. [FastAPI의 주요 기능 및 메서드 구현 예시](#2-FastAPI의-주요기능-및-메서드-구현예시)\
	3. 
4. 
5. 	
2-1. [파일 업로드](#1-파일-업로드)
2-2. [graphql 통합](#2-graphql-통합)
2-3. [데이터베이스 연동 sqlalchemy사용](#3-데이터베이스-연동-sqlalchemy-사용)
2-4. [인증 및 보안](#4-인증-및-보안)
2-5. [websocket통신](#5-websocket-통신)
2-6. [백그라운드작업](#6-백그라운드-작업)
2-7. [파일다운로드](#7-파일-다운로드)
2-8. [캐싱](#8-캐싱)
6. [FastAPI 사용 중요 기능 추천](#3-FastAPI-사용-중요-기능-추천)
7. [참고 항목](#4-참고항목)

#### # FastAPI 주요기능

##### 1. 빠른 성능
- FastAPI는 Starlette, Pydantic 기반 높은 성능 제공.
- Python의 가장 빠른 웹 프레임워크 중 하나, 대부분 다른 프레임워크 보다 뛰어난 속도.

##### 2. 자동 API 문서 생성
- **Swagger UI** 자동 생성 :  **/docs** 엔드포인트에서 대화형 API 문서 자동 제공.
- **ReDoc** 문서 지원 : **/redoc** 엔드포인트에서 추가 API 문서 제공.

##### 3. 강력한 데이터 검증
- **Pydantic 모델** 기반 데이터 검증 : 요청/응답 데이터 타입 힌트와 유효성 검사를 자동 수행.
- 복잡한 데이터 구조에 대한 쉬운 검증 / 자동 JSON 직렬화 및 역직렬화

##### 4. 타입 힌트 및 타입 체크
- Python 타입 힌트 완전 지원 / 정적 타입 체킹 통한 코드 안정성 향상 / IDE 자동 완성, 오류 감지 기능

##### 5. 의존성 주입 시스템
- 복잡한 의존성 관리 위한 강력한 의존성 주입 메커니즘 / 컴포넌트 간 결합도 낮추고 모듈성 높임.

##### 6. 보안 기능
- OAuth2 인증 및 JWT 토큰 지원 / CORS(Cross-Origin Resource Sharing) 미들웨어 내장
- HTTPS 및 보안 헤더 설정 용이

##### 7. 비동기 지원
- **async, await** 문법 완전 지원 / 비동기 요청 처리로 높은 성능 보장 / WebSocket 지원

##### 8. RESTful API 개발
- HTTP 메서드(GET, POST, PUT, DELETE 등) 쉬운 정의 / Path 파라미터, 쿼리 파라미터, 요청 본문 처리 용이

##### 9. 확장성
- 미들웨어 지원 / 다양한 데이터베이스와의 통합 용이 / OpenAPI(Swagger) 표준 지원

##### 10. 간단하고 직관적인 문법
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
```

##### 11. 추가 기능
- 파일 업로드 처리 / 백 그라운드 작업 지원 /  GraphQL 통합 / OpenTelemetry 지원


[목차로](#목차)

---

### 2. FastAPI의 주요기능 및 메서드 구현예시


##### 1. 파일 업로드
```python
from fastapi import FastAPI, File, UploadFile
from typing import List

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    # 단일 파일 업로드
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

@app.post("/multiple-files/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    # 다중 파일 업로드
    return {"file_names": [file.filename for file in files]}
```

##### 2. GraphQL 통합
```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
# pip install strawberry >> Error
# pip install strawberry-graphql >> 설치

# GraphQL 스키마 정의
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
```

##### 3. 데이터베이스 연동 (SQLAlchemy 사용)
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 모델 정의
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# 데이터베이스 세션 생성
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 의존성 함수
def get_db():
    db = SessionLocal()
    try:
	    # https://www.daleseo.com/python-yield/
	    # yield 키워드 사용시 제너레이터 반환 : return > 모든 값 메모리에 올림, yield > 결과 값을 하나씩 메모리에 올림.
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
```


##### 4. 인증 및 보안
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# >> pip install python-jose
from jose import jwt

# OAuth2 인증 스키마
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# 비밀 키와 알고리즘 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# 토큰 검증 함수
def verify_token(token: str):
    try:
        # 토큰 디코딩 로직 (JWT(JSON Web Token)를 해독 > 토큰에 포함된 정보를 추출)
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
```
```python
# 토큰생성, 디코딩, 사용예제
from jose import jwt

# 비밀 키와 알고리즘 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# 토큰 생성
def create_token(data: dict):
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 토큰 디코딩
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise ValueError("Invalid token")

# 사용 예제
if __name__ == "__main__":
    # 토큰에 포함할 데이터
    data = {"sub": "user_id", "name": "John Doe"}

    # 토큰 생성
    token = create_token(data)
    print("Generated Token:", token)

    # 토큰 디코딩
    try:
        decoded_data = decode_token(token)
        print("Decoded Data:", decoded_data)
    except ValueError as e:
        print(e)
```
##### * 로직 설명
1. 토큰 생성
    - create_token 함수는 주어진 데이터를 JWT로 인코딩.
    - 이때 SECRET_KEY와 ALGORITHM을 사용하여 토큰을 서명.
2. 토큰 디코딩
    - decode_token 함수는 주어진 JWT를 디코딩하여 원래의 데이터 추출
    - 이 과정에서
        - jwt.decode 함수는 토큰을 해독하고 서명을 검증.
        - 서명이 유효하지 않거나 토큰이 변조된 경우 jwt.JWTError 예외 발생.

* 주로 사용자 인증 및 권한 부여에 사용, 클라이언트와 서버 간 안전한 정보 전달.

##### * 비밀 키 설정
- 임의 설정 가능
    - 비밀 키는 사용자가 임의로 설정 할 수 있음.
    - 그러나 보안상의 이유로 충분히 복잡하고 예측 불가능한 문자열을 사용이 좋다.
    - 일반적으로 비밀 키는 환경 변수나 안전한 저장소에 보관하여 코드에 직접 노출되지 않도록 관리.

##### * 알고리즘 종류와 사용 방법
- JWT는 다양한 서명 알고리즘을 지원, 보안 수준과 사용 용도가 다름.
- 다음은 일반적 사용되는 알고리즘
    1. HS256 (HMAC with SHA-256)
        대칭 키 알고리즘으로, 비밀 키를 사용하여 토큰을 서명하고 검증합니다. 비밀 키가 양쪽(서버와 클라이언트) 모두에 필요합니다. 간단한 구현과 빠른 성능이 장점입니다.
    2. RS256 (RSA with SHA-256)
        비대칭 키 알고리즘으로, 공개 키와 비밀 키 쌍을 사용합니다. 비밀 키로 서명하고 공개 키로 검증합니다. 보안성이 높고, 공개 키를 클라이언트에 안전하게 배포할 수 있는 장점이 있습니다.
    3. ES256 (ECDSA with SHA-256)
        비대칭 키 알고리즘으로, RSA보다 더 작은 키 크기로 비슷한 보안 수준을 제공합니다. 성능이 뛰어나고, 모바일 환경에서 자주 사용됩니다.

* HS256 사용 예제:
    - 위의 코드에서 사용한 것처럼, HS256 알고리즘은 비밀 키를 사용하여 토큰을 생성하고 검증합니다.

* RS256 사용 예제:
```python
  from jose import jwt

  # 공개 키와 비밀 키 설정
  PRIVATE_KEY = "your_private_key"
  PUBLIC_KEY = "your_public_key"
  ALGORITHM = "RS256"

  # 토큰 생성
  def create_token(data: dict):
      token = jwt.encode(data, PRIVATE_KEY, algorithm=ALGORITHM)
      return token

  # 토큰 디코딩
  def decode_token(token: str):
      try:
          payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
          return payload
      except jwt.JWTError:
          raise ValueError("Invalid token")
```
1. RSA 키 쌍 생성
    - cryptography 라이브러리를 설치
    - 그런 다음, RSA 키 쌍을 생성.
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# RSA 키 쌍 생성
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# 비밀 키를 PEM 형식으로 직렬화
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# 공개 키를 PEM 형식으로 직렬화
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 키를 파일에 저장하거나 변수에 저장
with open("private_key.pem", "wb") as f:
    f.write(private_pem)

with open("public_key.pem", "wb") as f:
    f.write(public_pem)
```
2. JWT 생성 및 검증
    - 생성한 키를 사용하여 JWT를 생성, 검증.
```python
from jose import jwt

# 키 파일에서 읽기
with open("private_key.pem", "rb") as f:
    private_key = f.read()

with open("public_key.pem", "rb") as f:
    public_key = f.read()

ALGORITHM = "RS256"

# 토큰 생성
def create_token(data: dict):
    token = jwt.encode(data, private_key, algorithm=ALGORITHM)
    return token

# 토큰 디코딩
def decode_token(token: str):
    try:
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise ValueError("Invalid token")

# 사용 예제
if __name__ == "__main__":
    # 토큰에 포함할 데이터
    data = {"sub": "user_id", "name": "John Doe"}

    # 토큰 생성
    token = create_token(data)
    print("Generated Token:", token)

    # 토큰 디코딩
    try:
        decoded_data = decode_token(token)
        print("Decoded Data:", decoded_data)
    except ValueError as e:
        print(e)
```
##### * 설명
- RSA 키 생성
    cryptography 라이브러리를 사용하여 RSA 키 쌍을 생성합니다. 생성된 키는 PEM 형식으로 직렬화하여 파일에 저장하거나 메모리에 보관할 수 있습니다.
- JWT 생성 및 검증
    python-jose 라이브러리를 사용하여 RSA 비밀 키로 JWT를 서명하고, 공개 키로 검증합니다. 이 과정은 비대칭 암호화를 사용하여 보안을 강화합니다.

* 비대칭 암호화 사용, JWT를 안전하게 관리할 수 있게 함. 공개 키는 클라이언트에 배포하여 검증에 사용, 비밀 키는 서버에서 안전하게 보관.


##### 5. WebSocket 통신
```python
from fastapi import FastAPI, WebSocket

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
```

##### 6. 백그라운드 작업
```python
from fastapi import BackgroundTasks, FastAPI

def write_log(message: str):
    # 로그 작성 등의 백그라운드 작업
    with open("log.txt", mode="a") as log_file:
        log_file.write(message + "\n")

@app.post("/send-notification")
async def send_notification(background_tasks: BackgroundTasks):
    # 백그라운드 작업 추가
    background_tasks.add_task(write_log, "Notification sent")
    return {"status": "Notification sent"}
```

##### 7. 파일 다운로드
```python
from fastapi import FastAPI
from fastapi.responses import FileResponse

@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(
        path=f"./files/{filename}",
        filename=filename,
        media_type='application/octet-stream'
    )
```

##### 8. 캐싱
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

@app.get("/cached-data")
async def get_cached_data():
    return JSONResponse(
        content={"data": "some data"},
        headers={"Cache-Control": "public, max-age=3600"}
    )
```

[목차로](#목차)
---

### 3. FastAPI-사용-중요-기능-추천

##### 1. 요청 유효성 검사 (Validation)
- pydantic 참고 : https://data-newbie.tistory.com/836
```python
from fastapi import FastAPI, Query, Path, Body
# pydantic은 데이터 유효성 검사, 설정 라이브러리
from pydantic import BaseModel, Field

class UserModel(BaseModel):
	# Field 클래스 : 데이터모델 필드 정의 > 필드 유효성검사 규칙정의, 기본값설정
    username: str = Field(..., min_length=3, max_length=50)
    # email > 정규표현식 사용 유효성 검사
    email: str = Field(..., regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: int = Field(..., gt=0, lt=120)

@app.post("/users/")
def create_user(
    user: UserModel,
    q: str = Query(None, min_length=3, max_length=50),
    x: int = Path(..., gt=0)
):
    # 자동으로 데이터 유효성 검사
    return {"user": user, "query": q, "path": x}
```

##### 2. 예외 처리 (Exception Handling)
```python
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
	    # 예외 발생시키는 키워드, 특정 조건에서 오류를 명시적 발생시키거나, 기처리된 예외를 다시 발생시키는 데 사용
	    # raise 예외_클래스(메시지)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
            headers={"X-Error": "Error occurred"}
        )
    return {"item_id": item_id}

# 전역 예외 핸들러
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)}
    )
```
* Python에서 전역 예외 핸들러는 일반적으로 **비동기 프레임워크(예: FastAPI, Starlette)** 에서 사용됨. FastAPI와 같은 비동기 프레임워크의 예외 핸들러라면, 비동기 함수로 작성되었더라도 **await** 가 반드시 포함 되어야 하는 것은 아님.
* **async def** 로 정의된 함수는 비동기 함수로 간주, 호출 시 항상 await 가능 객체를 반환.
* **await** 는 비동기 작업 중단, 결과를 기다리기 위한 것, 함수 내부에서 동기적으로 실행할 코드만 있다면 await 가 없어도 됨.
* **JSONResponse**는 FastAPI의 동기적 동작이며, await가 필요 없음
* await 는 **비동기 작업(coroutine)** 또는 **awaitable 객체**에만 사용 가능.
- JSONResponse는 단순한 클래스 인스턴스화 동작을 수행하므로, 비동기 객체가 아님. > await 를 쓰면 오히려 에러 발생 가능(이 객체가 awaitable하지 않다는 예외(`TypeError: object is not awaitable`)를 발생)
- **await** some_async_function() # 예: 로깅 또는 외부 서비스 호출할때 사용


##### 3. 미들웨어 (Middleware)
- **CORS 미들웨어**는 프론트엔드와 백엔드가 다른 도메인에 있을 때, 요청 허용을 위해 사용.
- **커스텀 미들웨어**는 요청-응답 흐름에서 처리 시간 측정 또는 공통적 로직 추가를 위해 사용.

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# CORS 미들웨어 : 브라우저 보안정책 Same-Origin Policy 로 인해 발생하는 문제 해결을 위해 사용
app.add_middleware(
    CORSMiddleware,
	allow_origins=["*"], # 모든 도메인에서의 요청 허용
	allow_credentials=True, # 쿠키나 인증 정보를 포함한 요청 허용
	allow_methods=["*"], # 모든 HTTP 메서드 허용
	allow_headers=["*"], # 모든 헤더 허용
)

# 커스텀 미들웨어 : 요청(Request)과 응답(Response)의 처리를 커스터마이징
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
	start_time = time.time() # 요청 시작 시간 기록
	response = await call_next(request) # 다음 미들웨어 또는 실제 엔드포인트 호출
	process_time = time.time() - start_time # 처리 시간 계산
	response.headers["X-Process-Time"] = str(process_time) # 처리 시간을 응답 헤더에 추가
	return response
```

###### * CORS 미들웨어 사용 이유
- 클라이언트와 서버가 다른 도메인에 위치한 경우(예: 프론트엔드와 백엔드가 다른 URL 사용), CORS 설정이 없으면 브라우저에서 요청이 차단됨.
- 위 코드에서는 모든 도메인, 메서드, 헤더를 허용, API가 어디서든 접근 가능하게 설정됨.

###### * CORS 미들웨어 예시 시나리오
- 프론트엔드 애플리케이션이 `http://localhost:3000`에서 실행되고, 백엔드가 `http://localhost:8000`에 있다면, CORS를 설정하지 않으면 브라우저가 이 요청을 차단합니다.

###### * 커스텀 미들웨어 사용 이유
- **성능 측정**: 요청 처리 시간을 측정하여 성능 모니터링 가능.
- **응답 헤더 추가**: 요청/응답 흐름에 추가 데이터 삽입 또는 로그 기록.
- **공통 로직 처리**: 엔드포인트마다 중복 코드 작성 없이, 공통 작업(예: 인증, 로깅) 처리 가능

###### * 커스텀 미들웨어 예시 시나리오
- 클라이언트가 API에 요청을 보낼 때 응답 헤더에 **X-Process-Time** 이 추가되어, 해당 요청이 처리되는 데 걸린 시간 확인 가능.
- 이 데이터는 디버깅, 성능 최적화, 모니터링에 유용.

##### > 추가 : 별도 05.미들웨어 파일 확인


##### 4. 의존성 주입 (Dependency Injection)
```python
from fastapi import FastAPI, Depends, HTTPException
from typing import Optional

# 복잡한 의존성 주입
def common_parameters(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

# 의존성 체이닝
def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```
	# 복잡한 의존성 주입 설명
	4-1. q: Optional[str] = None
	- 타입: 선택적 문자열 (Optional String)
	- 기본값: None
	- 용도:
	    - 검색어나 쿼리 파라미터로 사용
	    - 값을 제공하지 않아도 기본적으로 None으로 처리
	    - 예: /items/?q=search_term

	4-2. skip: int = 0
	- 타입: 정수 (Integer)
	- 기본값: 0
	- 용도:
	    - 페이지네이션에서 건너뛸 아이템 수를 지정
	    - 데이터베이스 쿼리에서 오프셋으로 사용
	    - 예: /items/?skip=10은 처음 10개 아이템을 건너뜀

	4-3. limit: int = 100
	- 타입: 정수 (Integer)
	- 기본값: 100
	- 용도:
	    - 반환할 최대 아이템 수를 제한
	    - 페이지당 최대 데이터 수를 조절
	    - 예: /items/?limit=50은 최대 50개 아이템만 반환

###### * 실 예
```python
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {
        "q": commons['q'],
        "skip": commons['skip'],
        "limit": commons['limit']
    }

# 가능한 호출 방식들:
# 1. /items/ (모든 기본값 사용)
# 2. /items/?q=test (검색어 추가)
# 3. /items/?skip=20 (20개 건너뛰기)
# 4. /items/?limit=50 (50개로 제한)
# 5. /items/?q=test&skip=10&limit=20 (복합 사용)
```
###### * 의존성 채이닝 : Header(...) 세부 설명
1. x_token: str = Header(...)
	- Header(...) 는 HTTP 요청 헤더에서 특정 키의 값을 추출
	- `...(Ellipsis)` 는 해당 헤더가 반드시 존재해야 함을 의미
	- `x_token` 이라는 이름의 헤더를 필수로 요구
2. x_key: str = Header(...)
	- 마찬가지로 HTTP 요청 헤더에서 `x_key` 값을 추출
	- 해당 헤더가 반드시 존재해야 함
###### * 의존성 채이닝 의 작동 방식
1. `verify_token , verify_key` 함수 실행
    - `X-Token, X-Key` 헤더 검증
    - 토큰 or 키 유효하지 않으면 HTTPException 발생
2. 두 검증을 모두 통과하면 `read_items` 엔드포인트 실행

###### * 추가 예시 - 복잡한 채이닝
```python
def get_current_user(token: str = Depends(verify_token)):
    # 토큰을 기반으로 사용자 정보 조회
    user = find_user_by_token(token)
    return user

def check_user_permission(user = Depends(get_current_user)):
    # 사용자 권한 확인
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    return user

@app.get("/admin-items/")
async def get_admin_items(user = Depends(check_user_permission)):
    return {"admin_items": ["Item1", "Item2"]}

# 1. verify_token : 토큰 검증
# 2. get_current_user : 사용자 정보 조회
# 3. check_user_permission : 관리자 권한 확인
# 4. 모든 검증을 통과하면 관리자 전용 항목 반환
```

###### * 의존성 채이닝 : FastAPI에서 인증, 권한 부여, 데이터 검증 등 복잡 로직 모듈화, 재사용성을 만드는 강력한 패턴.
##### 5. 환경 설정 관리
```python
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Awesome API"
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()

@app.get("/info")
async def get_app_info():
    return {
        "app_name": settings.app_name,
        "database_url": settings.database_url
    }
```

##### 6. OpenAPI 커스터마이징
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

##### 7. 비동기 작업 (Async)
```python
import asyncio
from fastapi import FastAPI

@app.get("/long-running-task")
async def long_running_task():
    # 비동기 작업 수행
    await asyncio.sleep(5)  # 5초 대기
    return {"message": "Task completed"}
```

##### 8. 파라미터 타입 변환
```python
from fastapi import FastAPI, Path, Query
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(
    model_name: ModelName,
    version: int = Query(None, ge=1, le=10)
):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    return {"model_name": model_name, "version": version}
```

각 기능은 Python의 타입 힌트와 Pydantic의 강력한 검증 기능 활용, 코드의 안정성, 가독성을 높임.

[목차로](#목차)

### 4. 참고항목


#### C. 참고 항목

##### 공식 문서 및 참고 자료

1. **공식 문서**
   - FastAPI 공식 문서: https://fastapi.tiangolo.com/
   - GitHub 저장소: https://github.com/tiangolo/fastapi

2. **학습 리소스**
   - 공식 튜토리얼: https://fastapi.tiangolo.com/tutorial/
   - FastAPI 예제 모음: https://github.com/tiangolo/fastapi/tree/master/docs_src

##### 온라인 학습 플랫폼

1. **Udemy**
   - "FastAPI - The Complete Course" 같은 강의 제공
   - 실습 중심의 심화 학습 가능

2. **YouTube 강의**
   - Pyplane의 FastAPI 재생목록
   - Coding with Robby의 FastAPI 튜토리얼

##### 기술 블로그 및 커뮤니티

1. **Medium**
   - FastAPI 관련 심도 있는 기술 블로그 글들

2. **Real Python**
   - https://realpython.com/fastapi-python-web-apis/
   - 초보자부터 중급자까지 이해하기 쉬운 튜토리얼

##### GitHub 프로젝트 및 예제

1. **FastAPI 실제 프로젝트 예제**
   - https://github.com/rinarkou/fastapi-realworld-example-app
   - https://github.com/testdrivenio/fastapi-crud-async

##### 레퍼런스 및 추가 학습 자료

1. **공식 문서 섹션**
   - [Advanced User Guide](https://fastapi.tiangolo.com/advanced/)
   - [Deployment 가이드](https://fastapi.tiangolo.com/deployment/)

2. **Awesome FastAPI**
   - https://github.com/mjhea0/awesome-fastapi
   - FastAPI 관련 리소스 모음

##### 주요 참고 라이브러리

1. **Pydantic**
   - https://docs.pydantic.dev/
   - FastAPI의 데이터 검증에 핵심적인 라이브러리

2. **Starlette**
   - https://www.starlette.io/
   - FastAPI의 기반이 되는 비동기 웹 프레임워크


[목차로](#목차)
