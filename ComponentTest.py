"""
1. NumPy (완료)
2. Pandas (완료)
3. Requests
4. SQLAlchemy
5. FastAPI
6. Matplotlib
7. PyTest
8. Celery
9. Redis-py
10.Pillow (PIL)
"""

from common.NumpyCm import NumpyClass
from common.PandasCm import PandasCm

######################################################################################
# 컴포넌트 초기화
numpy_utils = NumpyClass()

# 배열 생성
array1 = numpy_utils.create_array([1, 2, 3, 4, 5])
array2 = numpy_utils.create_array([6, 7, 8, 9, 10])

# 행렬 연산
result = numpy_utils.matrix_operations(array1, array2, 'add')

# 통계 분석
stats = numpy_utils.statistical_analysis(array1)


######################################################################################
# 컴포넌트 초기화
pandas_utils = PandasCm()

# CSV 파일 읽기
#df = pandas_utils.read_data("port.csv", "csv")
df = pandas_utils.read_data("port.csv", "csv", encoding='utf-8', encoding_errors='ignore')

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

######################################################################################