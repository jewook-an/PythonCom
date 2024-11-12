import numpy as np
from typing import Union, List, Tuple, Optional
import logging

class CommonNumpy:
    """
    NumPy 관련 공통 기능을 제공하는 유틸리티 클래스
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def create_array(self, data: Union[List, Tuple], dtype: Optional[str] = None) -> np.ndarray:
        """
        리스트나 튜플로부터 NumPy 배열 생성
        
        Args:
            data: 변환할 데이터
            dtype: 데이터 타입 (예: 'float32', 'int64')
            
        Returns:
            numpy array
        """
        try:
            return np.array(data, dtype=dtype)
        except Exception as e:
            self.logger.error(f"배열 생성 중 오류 발생: {str(e)}")
            raise
            
    def matrix_operations(self, matrix_a: np.ndarray, matrix_b: np.ndarray, operation: str) -> np.ndarray:
        """
        행렬 연산 수행
        
        Args:
            matrix_a: 첫 번째 행렬
            matrix_b: 두 번째 행렬
            operation: 연산 종류 ('add', 'subtract', 'multiply', 'divide')
            
        Returns:
            계산된 결과 행렬
        """
        operations = {
            'add': np.add,
            'subtract': np.subtract,
            'multiply': np.multiply,
            'divide': np.divide
        }
        
        if operation not in operations:
            raise ValueError(f"지원하지 않는 연산입니다: {operation}")
            
        try:
            return operations[operation](matrix_a, matrix_b)
        except Exception as e:
            self.logger.error(f"행렬 연산 중 오류 발생: {str(e)}")
            raise
            
    def statistical_analysis(self, data: np.ndarray) -> dict:
        """
        기본적인 통계 분석 수행
        
        Args:
            data: 분석할 데이터 배열
            
        Returns:
            통계 분석 결과를 담은 딕셔너리
        """
        try:
            return {
                'mean': np.mean(data),
                'median': np.median(data),
                'std': np.std(data),
                'var': np.var(data),
                'min': np.min(data),
                'max': np.max(data)
            }
        except Exception as e:
            self.logger.error(f"통계 분석 중 오류 발생: {str(e)}")
            raise
            
    def matrix_decomposition(self, matrix: np.ndarray) -> dict:
        """
        행렬 분해 연산 수행
        
        Args:
            matrix: 분해할 행렬
            
        Returns:
            분해 결과를 담은 딕셔너리
        """
        try:
            return {
                'eigenvalues': np.linalg.eigvals(matrix),
                'svd': np.linalg.svd(matrix),
                'det': np.linalg.det(matrix) if matrix.shape[0] == matrix.shape[1] else None
            }
        except Exception as e:
            self.logger.error(f"행렬 분해 중 오류 발생: {str(e)}")
            raise
            
    def array_manipulation(self, array: np.ndarray, operation: str, **kwargs) -> np.ndarray:
        """
        배열 조작 작업 수행
        
        Args:
            array: 조작할 배열
            operation: 작업 종류 ('reshape', 'transpose', 'flatten', 'sort')
            **kwargs: 추가 매개변수
            
        Returns:
            조작된 배열
        """
        try:
            if operation == 'reshape':
                return array.reshape(kwargs.get('shape'))
            elif operation == 'transpose':
                return array.transpose()
            elif operation == 'flatten':
                return array.flatten()
            elif operation == 'sort':
                return np.sort(array, axis=kwargs.get('axis', None))
            else:
                raise ValueError(f"지원하지 않는 작업입니다: {operation}")
        except Exception as e:
            self.logger.error(f"배열 조작 중 오류 발생: {str(e)}")
            raise
            
    def linear_algebra(self, matrix_a: np.ndarray, matrix_b: Optional[np.ndarray] = None) -> dict:
        """
        선형 대수 연산 수행
        
        Args:
            matrix_a: 주 행렬
            matrix_b: 선택적 두 번째 행렬
            
        Returns:
            선형 대수 연산 결과를 담은 딕셔너리
        """
        try:
            results = {
                'rank': np.linalg.matrix_rank(matrix_a),
                'norm': np.linalg.norm(matrix_a),
                'inverse': np.linalg.inv(matrix_a) if matrix_a.shape[0] == matrix_a.shape[1] else None
            }
            
            if matrix_b is not None:
                results['dot_product'] = np.dot(matrix_a, matrix_b)
                
            return results
        except Exception as e:
            self.logger.error(f"선형 대수 연산 중 오류 발생: {str(e)}")
            raise
            
    def trigonometric_operations(self, angles: np.ndarray) -> dict:
        """
        삼각함수 연산 수행
        
        Args:
            angles: 각도 값을 담은 배열 (라디안)
            
        Returns:
            삼각함수 연산 결과를 담은 딕셔너리
        """
        try:
            return {
                'sin': np.sin(angles),
                'cos': np.cos(angles),
                'tan': np.tan(angles),
                'arcsin': np.arcsin(np.clip(angles, -1, 1)),
                'arccos': np.arccos(np.clip(angles, -1, 1)),
                'arctan': np.arctan(angles)
            }
        except Exception as e:
            self.logger.error(f"삼각함수 연산 중 오류 발생: {str(e)}")
            raise
