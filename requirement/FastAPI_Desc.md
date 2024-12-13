#### 목차
* * FastAPI 주요 기능
* A. FastAPI의 주요 기능 및 메서드 구현 예시
* B. FastAPI 사용 중요 기능 추천.
* C. 참고 항목
### 목차

1. [FastAPI주요기능](#1-FastAPI주요기능)
2. [FastAPI의 주요 기능 및 메서드 구현 예시](#2-FastAPI의주요기능및메서드구현예시)
3. [FastAPI 사용 중요 기능 추천](#3-FastAPI사용중요기능추천)
4. [참고 항목](#4-참고항목)


#### # FastAPI 주요 기능

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

