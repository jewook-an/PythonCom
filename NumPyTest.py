from common import NumpyClass
import numpy as np

# 컴포넌트 초기화
numpy_utils = NumpyClass()

# 배열 생성
array1 = numpy_utils.create_array([1, 2, 3, 4, 5])
array2 = numpy_utils.create_array([6, 7, 8, 9, 10])

# 행렬 연산
result = numpy_utils.matrix_operations(array1, array2, 'add')
print(result)

# 통계 분석
stats = numpy_utils.statistical_analysis(array1)
print(stats)

# NumPy의 기본적인 통계 및 수학 함수들을 설명해드리겠습니다. 이 함수들은 데이터 분석에서 매우 자주 사용되는 핵심 기능들입니다.
# 1. 기본 통계 함수들:
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 중심 경향값(Central Tendency)
print(f"평균(mean): {np.mean(arr)}")                   # 산술 평균
print(f"중앙값(median): {np.median(arr)}")             # 중앙값
print(f"최빈값(mode): {np.bincount(arr).argmax()}")    # 최빈값

# 분산도(Variance & Spread)
print(f"표준편차(std): {np.std(arr)}")      # 표준편차
print(f"분산(var): {np.var(arr)}")          # 분산
print(f"최소값(min): {np.min(arr)}")        # 최솟값
print(f"최대값(max): {np.max(arr)}")        # 최댓값
print(f"범위(range): {np.ptp(arr)}")        # 최대값 - 최소값

# 위치 측정
print(f"최소값 위치: {np.argmin(arr)}")     # 최솟값의 인덱스
print(f"최대값 위치: {np.argmax(arr)}")     # 최댓값의 인덱스

# 2. 수학 함수들:
# 기본 수학 연산
print(f"합계: {np.sum(arr)}")               # 합계
print(f"누적 합계: {np.cumsum(arr)}")       # 누적 합계
print(f"곱: {np.prod(arr)}")                # 모든 원소의 곱
print(f"누적 곱: {np.cumprod(arr)}")        # 누적 곱

# 반올림 함수들
print(f"반올림: {np.round(3.14159, 2)}")    # 소수점 반올림
print(f"올림: {np.ceil(3.14)}")             # 올림
print(f"내림: {np.floor(3.14)}")            # 내림

# 3. 배열 조작 함수들:
# 배열 형태 변경
arr_2d = arr.reshape(2, 5)                  # 1차원을 2차원으로 변경
print(f"전치: {arr_2d.transpose()}")        # 행과 열 바꾸기

# 배열 연결
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
print(f"수평 연결: {np.hstack((arr1, arr2))}")  # 수평으로 연결
print(f"수직 연결: {np.vstack((arr1, arr2))}")  # 수직으로 연결

# 4. 조건부 함수들:
# 조건부 연산
print(f"조건에 맞는 값 찾기: {np.where(arr > 5)}")  # 5보다 큰 값의 인덱스
print(f"조건에 맞는 값 선택: {np.extract(arr > 5, arr)}")  # 5보다 큰 값들

# 정렬
print(f"정렬: {np.sort(arr)}")              # 오름차순 정렬
print(f"역순 정렬: {np.sort(arr)[::-1]}")   # 내림차순 정렬

# 5. 집계 함수들:
# 다양한 집계 방법
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"행 방향 평균: {np.mean(arr_2d, axis=0)}")  # 각 열의 평균
print(f"열 방향 평균: {np.mean(arr_2d, axis=1)}")  # 각 행의 평균
print(f"전체 평균: {np.mean(arr_2d)}")             # 전체 평균

# 6. 고급 통계 함수들:
# 상관관계와 공분산
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([2, 4, 5, 4, 5])
print(f"상관계수: {np.corrcoef(arr1, arr2)}")     # 상관계수
print(f"공분산: {np.cov(arr1, arr2)}")            # 공분산

# 백분위수
print(f"사분위수: {np.percentile(arr, [25, 50, 75])}") # 25%, 50%, 75% 백분위수

"""
이러한 함수들의 주요 특징:
1. 대부분의 함수들은 axis 매개변수를 지원하여 다차원 배열에서 특정 축을 따라 연산 가능
2. 결측값(NaN)을 처리하는 버전도 존재 (예: nanmean, nanstd 등)
3. 대부분의 함수들이 배열 전체 또는 부분에 대해 작동 가능
4. 계산 효율성이 매우 높음 (C로 구현되어 있음)
"""

# 실제 사용 시 유용한 팁:
# 여러 통계량 한번에 계산
def describe_array(arr):
    return {
        'mean': np.mean(arr),
        'median': np.median(arr),
        'std': np.std(arr),
        'var': np.var(arr),
        'min': np.min(arr),
        'max': np.max(arr),
        'range': np.ptp(arr),
        'q1': np.percentile(arr, 25),
        'q3': np.percentile(arr, 75)
    }

# 사용 예시
data = np.random.normal(0, 1, 1000)  # 정규분포 데이터 생성
stats = describe_array(data)
for key, value in stats.items():
    print(f"{key}: {value}")

# 이 함수들은 데이터분석, 과학계산, 머신러닝 등 여러 분야에서 기본 및 필수 도구로 사용.

