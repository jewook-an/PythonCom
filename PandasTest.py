# 컴포넌트 초기화
pandas_utils = CommonPandas()

# CSV 파일 읽기
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
