** 프로젝트 구조 **


## common 폴더 구조 및 파일 설명

common 폴더에는 여러 컴포넌트들이 구현되어 있습니다. 각 컴포넌트는 특정 라이브러리나 기능을 추상화하여 제공합니다.

### 폴더 구조
- common/
  - FastapiCm.py
  - NumpyClass.py
  - PandasCm.py
  - SQLalchemyCm.py
  - RedisCm.py (pip install redis)
  - PillowCm.py (pip install Pillow)

### 파일 설명
- FastapiCm.py
  - FastAPI 프레임워크 활용, API 개발을 위한 컴포넌트.
  - 데이터베이스 연결, 인증, 예외 처리 등의 기능 제공.

- NumpyClass.py
  - NumPy 라이브러리 활용, 수치 계산 및 배열 조작을 위한 컴포넌트.
  - 배열 생성, 행렬 연산, 통계 분석 등의 기능 제공.

- PandasCm.py
  - Pandas 라이브러리 활용, 데이터 분석 및 조작을 위한 컴포넌트.
  - 데이터 읽기/쓰기, 데이터 클리닝, 변환, 분석 등의 기능 제공.

- SQLalchemyCm.py
  - SQLAlchemy 라이브러리 활용, 데이터베이스 연결 및 쿼리 실행을 위한 컴포넌트.
  - 데이터베이스 세션 관리, 쿼리 실행, 예외 처리 등의 기능 제공.

- RedisCm.py
  - Redis 라이브러리 활용, 인메모리 캐시 및 데이터 저장소 관리를 위한 컴포넌트.
  - 키-값 저장, 데이터 만료 설정, 리스트/셋/해시 등의 데이터 구조 조작, 캐싱 기능 제공.

- PillowCm.py
  - Pillow 라이브러리 활용, 이미지 처리를 위한 컴포넌트.
  - 이미지 로드, 저장, 크기 조정, 필터 적용 등의 기능 제공.

