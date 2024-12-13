from PythonCom.common.NumpyCm import NumpyClass
from PythonCom.common.PandasCm import PandasCm

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
# 컴포넌트 초기화 : Rainbow CSV 확장 프로그램 설치
pandas_utils = PandasCm()

# CSV 파일 읽기
# df = pandas_utils.read_data("port.csv", "csv")
df = pandas_utils.read_data("port.csv", "csv", encoding='utf-8', encoding_errors='ignore')
"""
1. 파일 인코딩 확인: 일반적으로 ISO-8859-1, Windows-1252, UTF-16
2. 다른 인코딩으로 읽기: 파일Read 인코딩 지정, 예 > ISO-8859-1로 Read 시
   with open('your_file.txt', 'r', encoding='ISO-8859-1') as file:
       content = file.read()
3. 바이트로 읽기: 바이트 모드 Read, 필요시 수동 디코딩. 예 >
   with open('your_file.txt', 'rb') as file:
       byte_content = file.read()
       content = byte_content.decode('ISO-8859-1')  # 또는 다른 인코딩
4. 에러 처리 옵션 사용: 디코딩 중 오류 무시, 대체 문자 사용 설정. 예 >
    with open('your_file.txt', 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    or
    with open('your_file.txt', 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
"""

# 데이터 클리닝
clean_df = pandas_utils.data_cleaning(df,
    operations=['remove_duplicates', 'fill_na'],
    fill_value=0
)

# 데이터 변환
transformed_df = pandas_utils.data_transformation(
    clean_df,
    #columns=['Source', 'IP'],
    columns=['Source', 'IP', 'Destination', 'IP', 'Protocol', 'Port', '방향', '용도'],
    operation='normalize'
)

# 데이터 분석
analysis_results = pandas_utils.data_analysis(transformed_df)

######################################################################################