** 프로젝트 구조 **


## common 폴더 구조 및 파일 설명

common 폴더에는 여러 컴포넌트들이 구현되어 있습니다. 각 컴포넌트는 특정 라이브러리나 기능을 추상화하여 제공합니다.

### 폴더 구조
- common/
  - FastapiCm.py
  - NumpyClass.py
  - PandasCm.py
  - SQLalchemyCm.py

### 파일 설명
- FastapiCm.py: FastAPI 프레임워크를 활용한 API 개발을 위한 컴포넌트입니다. 데이터베이스 연결, 인증, 예외 처리 등의 기능을 제공합니다.

- NumpyClass.py: NumPy 라이브러리를 활용한 수치 계산 및 배열 조작을 위한 컴포넌트입니다. 배열 생성, 행렬 연산, 통계 분석 등의 기능을 제공합니다.

- PandasCm.py: Pandas 라이브러리를 활용한 데이터 분석 및 조작을 위한 컴포넌트입니다. 데이터 읽기/쓰기, 데이터 클리닝, 변환, 분석 등의 기능을 제공합니다.

- SQLalchemyCm.py: SQLAlchemy 라이브러리를 활용한 데이터베이스 연결 및 쿼리 실행을 위한 컴포넌트입니다. 데이터베이스 세션 관리, 쿼리 실행, 예외 처리 등의 기능을 제공합니다.

이러한 컴포넌트들은 프로젝트 전반에서 공통적으로 사용되는 기능들을 모듈화하여 코드의 재사용성을 높이고 개발 효율성을 향상시키는 데 도움을 줍니다. 각 컴포넌트는 해당 라이브러리의 기능을 추상화하여 제공함으로써 사용자가 좀 더 쉽게 해당 기능을 활용할 수 있도록 합니다.