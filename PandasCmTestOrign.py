
from common import PandasCm
import numpy as np

# 컴포넌트 초기화
pandas_utils = PandasCm()

# CSV 파일 읽기 >> Try~Catch 로 못읽을시 Error 처리
# def read_data(self, file_path: Union[str, Path], file_type: str, **kwargs) -> pd.DataFrame:
df = pandas_utils.read_data("data.csv", "csv")

# 데이터 클리닝
clean_df = pandas_utils.data_cleaning(df, 
    operations=['remove_duplicates', 'fill_na'],
    fill_value=0
)

# 데이터 변환
transformed_df = pandas_utils.data_transformation(
    clean_df,
    columns=['column1', 'column2'],
    operation='normalize'
)

# 데이터 분석
analysis_results = pandas_utils.data_analysis(transformed_df)

"""
**kwargs 는 키워드 인자(keyword arguments)를 딕셔너리 형태로 받는 Python 특별 매개변수.
Pandas 내 활용 실제예제 참고 : 예로, CommonPandas 클래스의 여러 메서드에서 **kwargs의 사용예제를 확인.
"""

# 1. read_data 메서드 사용 예제:
# pandas_utils = CommonPandas()

# 기본적인 CSV 읽기
df1 = pandas_utils.read_data("data.csv", "csv")

# kwargs를 사용한 다양한 옵션 지정
df2 = pandas_utils.read_data(
    "data.csv", 
    "csv",
    encoding='utf-8',                # 인코딩 지정
    sep=';',                        # 구분자 지정
    skiprows=2,                     # 처음 2줄 건너뛰기
    usecols=['name', 'age', 'city'], # 특정 열만 읽기
    na_values=['NA', 'missing']     # NA로 처리할 값들 지정
)

# Excel 파일 읽기 시 kwargs 활용
df3 = pandas_utils.read_data(
    "data.xlsx",
    "excel",
    sheet_name='Sheet2',           # 특정 시트 지정
    skiprows=1,                    # 첫 행 건너뛰기
    header=None,                   # 헤더 없음
    names=['Col1', 'Col2', 'Col3'] # 열 이름 직접 지정
)

# 2. data_cleaning 메서드 사용 예제:
# 기본적인 데이터 클리닝
clean_df1 = pandas_utils.data_cleaning(
    df, 
    operations=['remove_duplicates', 'fill_na']
)

# kwargs를 사용한 상세 옵션 지정
clean_df2 = pandas_utils.data_cleaning(
    df,
    operations=['remove_duplicates', 'fill_na', 'drop_na', 'reset_index'],
    duplicate_options={
        'subset': ['name', 'age'],    # 특정 열만 고려하여 중복 제거
        'keep': 'first'               # 중복 시 첫 번째 행 유지
    },
    fill_value={                      # 열별로 다른 값으로 NA 채우기
        'age': 0,
        'income': df['income'].mean(),
        'category': 'unknown'
    },
    dropna_options={
        'subset': ['important_column'], # 특정 열의 NA만 고려
        'thresh': 3                     # 최소 3개 이상의 유효값이 있는 행만 유지
    }
)

# 3. data_transformation 메서드 사용 예제:
# 기본적인 데이터 변환
trans_df1 = pandas_utils.data_transformation(
    df,
    columns=['age', 'income'],
    operation='normalize'
)

# kwargs를 사용한 날짜 변환 옵션
trans_df2 = pandas_utils.data_transformation(
    df,
    columns=['date_column'],
    operation='datetime_convert',
    datetime_options={
        'format': '%Y-%m-%d',        # 날짜 형식 지정
        'errors': 'coerce',          # 변환 실패 시 NA로 처리
        'utc': True                  # UTC 시간으로 변환
    }
)

# 4. data_filtering 메서드 사용 예제:
# 복잡한 필터링 조건 지정
filtered_df = pandas_utils.data_filtering(
    df,
    conditions={
        'age': {
            'operator': '>',
            'value': 25
        },
        'income': {
            'operator': 'between',
            'value': [30000, 50000]
        },
        'city': {
            'operator': 'in',
            'value': ['Seoul', 'Busan', 'Incheon']
        }
    }
)

# 5. save_data 메서드 사용 예제:
# CSV 저장 시 kwargs 활용
pandas_utils.save_data(
    df,
    "output.csv",
    "csv",
    index=False,                # 인덱스 제외
    encoding='utf-8-sig',      # 한글 지원 인코딩
    sep=';',                   # 구분자 지정
    float_format='%.2f'        # 소수점 둘째자리까지 표시
)

# Excel 저장 시 kwargs 활용
pandas_utils.save_data(
    df,
    "output.xlsx",
    "excel",
    sheet_name='Report',       # 시트 이름 지정
    index=False,               # 인덱스 제외
    freeze_panes=(1,0),        # 첫 행 고정
    engine='openpyxl'         # Excel 엔진 지정
)

"""
**kwargs의 장점:
1. 유연성 : 함수를 수정 하지않고 다양한 옵션 전달 가능.
2. 확장성 : 새로운 옵션 필요시 함수 수정 없이 사용 가능.
3. 코드재사용성 : 다양한 상황에서 같은 함수를 다르게 활용이 가능함.

실사용시 각 메서드의 문서화된 옵션 참고해 필요한 kwargs를 전달 하면 됨.
"""
