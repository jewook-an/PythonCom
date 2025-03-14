# PythonCom

### 목차

1. [NumPy](#1-NumPy)
2. [Pandas](#2-Pandas)
3. [Requests](#3-Requests)
4. [SQLAlchemy](#4-SQLAlchemy)
5. [FastAPI](#5-FastAPI)
6. [Matplotlib](#6-Matplotlib)
7. [PyTest](#7-PyTest)
8. [Celery](#8-Celery)
9. [Redis-py](#9-Redis-py)

10.[Pillow (PIL)](#10-Pillow-Pil)

##### 추가 항목

 - PyGame
   - https://sylagape1231.tistory.com/25
   - https://pygame.readthedocs.io/en/latest/1_intro/intro.html
 - PyBrain
 - Statsmodels
 - TensorFlow
 - Seaborn
 - Scrapy
 - PyTorch
 - SciPy
 - Keras
 - Scikit-learn

###### install 내역 (최종 확인 필요)
1. pip install numpy
2. pip install pandas
3. pip install requests
4. pip install sqlalchemy
5. pip install fastapi
6. pip install jwt
7. pip install celery
8. pip install redis
9. pip install pytest
10. pip install matplotlib
11. pip install pillow


파이썬 라이브러리 중 유용하고 널리 사용되는  10가지를 선정

#### 1. NumPy
- 특징: 수치 계산을 위한 기본 라이브러리
- 주요 기능:
  * 다차원 배열 처리
  * 선형 대수 연산
  * 행렬 계산
- 컴포넌트 활용: 데이터 처리 및 수치 계산 유틸리티

* 주요 기능

  1. create_array: 리스트나 튜플을 NumPy 배열로 변환
  2. matrix_operations: 기본적인 행렬 연산 (덧셈, 뺄셈, 곱셈, 나눗셈)
  3. statistical_analysis: 기본 통계 분석 (평균, 중앙값, 표준편차 등)
  4. matrix_decomposition: 행렬 분해 연산 (고유값, SVD, 행렬식)
  5. array_manipulation: 배열 조작 (reshape, transpose, flatten, sort)
  6. linear_algebra: 선형 대수 연산 (rank, norm, inverse, dot product)
  7. trigonometric_operations: 삼각함수 연산

* NumPy 컴포넌트 특징
  1. 타입 힌팅을 사용하여 코드의 가독성과 유지보수성 향상
  2. 예외 처리와 로깅을 통한 안정적인 에러 핸들링
  3. 모듈화된 구조로 쉬운 확장성
  4. 문서화된 함수로 사용법 이해가 용이

#### 2. Pandas
- 특징: 데이터 분석과 조작을 위한 라이브러리
- 주요 기능:
  * DataFrame을 통한 데이터 구조화
  * 데이터 필터링, 그룹화, 병합
  * CSV, Excel 파일 처리
- 컴포넌트 활용: 데이터 처리 및 분석 컴포넌트

* 주요 기능

  1. read_data: 다양한 형식(CSV, Excel, JSON, SQL)의 데이터 파일 읽기
  2. save_data: DataFrame을 다양한 형식으로 저장
  3. data_cleaning: 데이터 클리닝 작업 (중복 제거, NA 처리 등)
  4. data_transformation: 데이터 변환 (정규화, 표준화, 범주형 인코딩 등)
  5. data_analysis: 기본적인 데이터 분석 (기술 통계, 상관관계 등)
  6. data_grouping: 데이터 그룹화 및 집계
  7. data_filtering: 조건에 따른 데이터 필터링

* Pandas 컴포넌트 특징
  1. 다양한 파일 형식 지원
  2. 유연한 데이터 처리 옵션
  3. 체계적인 예외 처리와 로깅
  4. 타입 힌팅을 통한 코드 가독성 향상
  5. 모듈화된 구조로 확장 용이

* 추가, 수정 기능이 필요시 확인.
  1. 시계열 데이터 처리 기능
  2. 피벗 테이블 생성 기능
  3. 데이터 시각화 관련 기능
  4. 데이터 결합(merge, join, concat) 기능
  5. 문자열 처리 기능

[목차로](#목차)

#### 3. Requests
- 특징: HTTP 통신을 위한 라이브러리
- 주요 기능:
  * HTTP 요청 처리 (GET, POST 등)
  * API 통신
  * 세션 관리
- 컴포넌트 활용: API 통신 래퍼 컴포넌트

* 주요 기능

  1. 기본 HTTP 메소드:
     - GET, POST, PUT, DELETE 요청 처리
     - JSON 데이터 자동 처리
     - 쿼리 파라미터 및 요청 바디 지원

  2. 파일 처리:
     - 파일 업로드
     - 파일 다운로드 (스트리밍 지원)

  3. 설정 관리:
     - 커스텀 헤더 설정
     - 기본 인증 설정
     - 타임아웃 설정

  4. 에러 처리:
     - HTTP 에러 자동 감지
     - JSON 디코딩 에러 처리
     - 로깅 기능

* 추가, 수정 기능이 필요시 확인.
  1. 재시도(retry) 메커니즘 추가
  2. 캐싱 기능 구현
  3. 비동기 요청 지원
  4. 특정 API에 맞춘 커스텀 메소드 추가​​​​​​​​​​​​​​​​

[목차로](#목차)

#### 4. SQLAlchemy
- 특징: SQL 데이터베이스 ORM
- 주요 기능:
  * 데이터베이스 모델링
  * SQL 쿼리 생성 및 실행
  * 다양한 데이터베이스 지원
- 컴포넌트 활용: 데이터베이스 접근 컴포넌트

* 주요 기능

  1. 기본 CRUD 작업:
     - 생성 (단일/일괄)
     - 조회 (ID/전체/필터링)
     - 업데이트
     - 삭제

  2. 세션 관리:
     - 컨텍스트 매니저를 통한 안전한 세션 관리
     - 자동 커밋/롤백 처리

  3. 고급 기능:
     - Raw SQL 쿼리 실행
     - 대량 데이터 삽입
     - 페이지네이션
     - 필터링

  4. 에러 처리:
     - SQLAlchemy 예외 처리
     - 로깅 기능

* 추가, 수정 기능이 필요시 확인.
  1. 관계(relationship) 처리 기능
  2. 마이그레이션 지원
  3. 비동기 쿼리 지원
  4. 캐싱 메커니즘
  5. 더 세밀한 쿼리 빌더 기능​​​​​​​​​​​​​​​​

[목차로](#목차)

#### 5. FastAPI
- 특징: 현대적인 웹 API 프레임워크
- 주요 기능:
  * 비동기 처리
  * 자동 API 문서화
  * 타입 힌팅 지원
- 컴포넌트 활용: API 엔드포인트 컴포넌트

* 주요 기능

  1. 기본 CRUD 작업:
     - 생성, 조회, 수정, 삭제 엔드포인트
     - 페이지네이션 지원
     - 타입 안전성을 위한 제네릭 타입 사용

  2. 보안 기능:
     - JWT 기반 인증
     - OAuth2 지원
     - 토큰 생성 및 검증

  3. 예외 처리:
     - 글로벌 예외 핸들러
     - HTTP 예외 처리
     - 유효성 검사 예외 처리

  4. 미들웨어:
     - CORS 지원
     - 요청 로깅
     - 성능 모니터링

  5. 구조화된 응답:
     - 페이지네이션 응답 모델
     - 표준화된 에러 응답
     - Pydantic 모델 기반 스키마

* 추가, 수정 기능이 필요시 확인.
  1. WebSocket 지원
  2. 백그라운드 태스크
  3. 캐시 미들웨어
  4. 파일 업로드 처리
  5. API 문서화 커스터마이징
  6. 레이트 리미팅
  7. 데이터 검증 추가​​​​​​​​​​​​​​​​

[목차로](#목차)

#### 6. Matplotlib
- 특징: 데이터 시각화 라이브러리
- 주요 기능:
  * 다양한 그래프 생성
  * 차트 커스터마이징
  * 이미지 저장
- 컴포넌트 활용: 데이터 시각화 컴포넌트

* 주요 기능

  1. 기본 차트 유형:
     - 선 그래프
     - 산점도
     - 막대 그래프
     - 히스토그램
     - 박스 플롯
     - 히트맵
     - 파이 차트
     - 시계열 그래프
     - 상관관계 행렬

  2. 커스터마이징 옵션:
     - 그래프 크기 및 해상도
     - 색상 팔레트
     - 축 레이블 및 제목
     - 그리드 및 범례
     - 날짜 형식

  3. 유틸리티 기능:
     - 파일 저장
     - Base64 인코딩
     - 메모리 관리
     - 스타일 관리

  4. 데이터 지원:
     - Pandas DataFrame
     - NumPy 배열
     - Python 딕셔너리
     - 리스트

* 추가, 수정 기능이 필요시 확인.
  1. 3D 플롯 지원
  2. 애니메이션 기능
  3. 서브플롯 지원
  4. 더 많은 차트 유형
  5. 인터랙티브 기능
  6. 커스텀 테마 지원
  7. 통계 분석 기능 통합​​​​​​​​​​​​​​​​

[목차로](#목차)

#### 7. PyTest
- 특징: 테스트 프레임워크
- 주요 기능:
  * 단위 테스트
  * 픽스처 지원
  * 파라미터화된 테스트
- 컴포넌트 활용: 테스트 유틸리티 컴포넌트

* 주요 기능

  1. **기본 구성 요소**:
     - `TestConfig`: 테스트 환경 설정 관리
     - `BasePage`: Page Object Model 패턴 구현
     - `TestDataManager`: 테스트 데이터 관리

  2. **pytest 기능**:
     - 커스텀 마커 (`@pytest.mark.smoke` 등)
     - 픽스처 (`test_config`, `test_data_manager`)
     - 파라미터화된 테스트
     - 자동 설정/정리 (setup/teardown)

  3. **유틸리티 기능**:
     - 로깅 시스템
     - 스크린샷 캡처
     - 조건 대기
     - 테스트 결과 리포팅

  4. **확장성**:
     - 새로운 테스트 케이스 쉽게 추가 가능
     - 커스텀 리포터로 결과 관리
     - 모듈화된 구조


[목차로](#목차)

#### 8. Celery
- 특징: 분산 태스크 큐
- 주요 기능:
  * 비동기 작업 처리
  * 작업 스케줄링
  * 분산 처리
- 컴포넌트 활용: 백그라운드 작업 처리 컴포넌트

* 주요 기능

  1. **기본 구성 요소**:
     - `CeleryConfig`: Celery 기본 설정 관리
     - `RedisManager`: Redis 연결 및 상태 관리
     - `TaskLogger`: 작업 로깅 시스템
     - `BaseTask`: 기본 작업 클래스

  2. **고급 기능**:
     - 작업 재시도 데코레이터 (`@retry_on_failure`)
     - 성능 측정 데코레이터 (`@measure_performance`)
     - 작업 스케줄러 (`TaskScheduler`)
     - 작업 모니터링 (`TaskMonitor`)

  3. **에러 처리 및 로깅**:
     - 컨텍스트 매니저를 통한 에러 처리
     - 상세한 로깅 시스템
     - Redis를 통한 작업 상태 추적

  4. **시그널 처리**:
     - 작업 전송 후 처리
     - 작업 실행 전 처리
     - 성공/실패 시 처리


* Celery 프레임워크 이점 *
  1. 작업의 안정적인 실행과 모니터링
  2. 상세한 로깅과 에러 처리
  3. 유연한 스케줄링
  4. 성능 측정과 최적화
  5. 확장 가능한 구조


[목차로](#목차)

#### 9. Redis-py
- 특징: Redis 클라이언트 라이브러리
- 주요 기능:
  * 캐시 처리
  * 세션 관리
  * 메시지 큐
- 컴포넌트 활용: 캐시 관리 컴포넌트

* 주요 기능
  1. **핵심 기능**:
     - `RedisConnectionPool`: 연결 풀 관리
     - `RedisCache`: 캐싱 시스템
     - `RedisLock`: 분산 락 관리
     - `RedisQueue`: 메시지 큐 구현
     - `RedisPubSub`: 발행/구독 시스템
     - `RedisRateLimiter`: 속도 제한 관리
     - `RedisDataManager`: 데이터 CRUD 관리
     - `RedisHealthCheck`: 상태 모니터링

  2. **유틸리티 기능**:
     - 캐시 데코레이터
     - 키 생성 및 관리
     - 직렬화/역직렬화
     - 로깅 시스템

  3. **고급 기능**:
     - 컨텍스트 매니저를 통한 락 관리
     - 타임아웃 및 재시도 메커니즘
     - 배치 처리 지원
     - 헬스 체크 및 모니터링

* Redis-py 프레임워크 이점 *
  1. 통합된 Redis 기능 관리
  2. 안전한 연결 풀 관리
  3. 편리한 캐싱 시스템
  4. 분산 환경에서의 동기화
  5. 유연한 메시지 처리
  6. 효율적인 속도 제한
  7. 상세한 모니터링


[목차로](#목차)

#### 10. Pillow (PIL)
- 특징: 이미지 처리 라이브러리
- 주요 기능:
  * 이미지 변환 및 필터링
  * 이미지 포맷 변환
  * 이미지 리사이징
- 컴포넌트 활용: 이미지 처리 유틸리티 컴포넌트

* 주요 기능

1. **단일 이미지 처리**
   - 리사이징 (fit/fill)
   - 필터 적용 (밝기, 대비, 채도, 블러)
   - 이미지 변환 (회전, 뒤집기)
   - 텍스트/도형 추가
   - 워터마크 추가

2. **이미지 분석**
   - 색상 히스토그램
   - 주요 색상 추출
   - 평균 밝기 계산

3. **배치 처리**
   - 여러 이미지를 한 번에 처리
   - 여러 작업을 순차적으로 적용

4. **이미지 최적화**
   - 압축
   - 형식 변환
   - 색상 수 감소

사용시:
1. 입력 이미지를 준비 및 경로 설정.
2. 출력 디렉토리를 생성.
3. 필요한 파라미터의 조정.
4. 스크립트를 실행.

[목차로](#목차)

* codesandbox연결시_설치
![alt text](./images/VSCode_Remote_SSH.png)

* Python 빌드 및 테스트
https://docs.github.com/ko/actions/use-cases-and-examples/building-and-testing/building-and-testing-python