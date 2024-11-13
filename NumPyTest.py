# 컴포넌트 초기화
numpy_utils = CommonNumpy()

# 배열 생성
array1 = numpy_utils.create_array([1, 2, 3, 4, 5])
array2 = numpy_utils.create_array([6, 7, 8, 9, 10])

# 행렬 연산
result = numpy_utils.matrix_operations(array1, array2, 'add')

# 통계 분석
stats = numpy_utils.statistical_analysis(array1)
