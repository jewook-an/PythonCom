import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional
import logging
from pathlib import Path
import io

class PandasCm:
    """
    Pandas 관련 공통 기능을 제공하는 유틸리티 클래스
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def read_data(self, file_path: Union[str, Path], file_type: str, **kwargs) -> pd.DataFrame:
        """
        다양한 형식의 파일을 DataFrame으로 읽기
        
        Args:
            file_path: 파일 경로
            file_type: 파일 타입 ('csv', 'excel', 'json', 'sql')
            **kwargs: 추가 읽기 옵션
            
        Returns:
            pandas DataFrame
        """
        try:
            readers = {
                'csv': pd.read_csv,
                'excel': pd.read_excel,
                'json': pd.read_json,
                'sql': pd.read_sql
            }
            
            if file_type not in readers:
                raise ValueError(f"지원하지 않는 파일 타입입니다: {file_type}")
                
            return readers[file_type](file_path, **kwargs)
        except Exception as e:
            self.logger.error(f"파일 읽기 중 오류 발생: {str(e)}")
            raise
            
    def save_data(self, df: pd.DataFrame, file_path: Union[str, Path], file_type: str, **kwargs) -> None:
        """
        DataFrame을 다양한 형식으로 저장
        
        Args:
            df: 저장할 DataFrame
            file_path: 저장할 경로
            file_type: 저장 형식 ('csv', 'excel', 'json')
            **kwargs: 추가 저장 옵션
        """
        try:
            writers = {
                'csv': df.to_csv,
                'excel': df.to_excel,
                'json': df.to_json
            }
            
            if file_type not in writers:
                raise ValueError(f"지원하지 않는 파일 타입입니다: {file_type}")
                
            writers[file_type](file_path, **kwargs)
        except Exception as e:
            self.logger.error(f"파일 저장 중 오류 발생: {str(e)}")
            raise
            
    def data_cleaning(self, df: pd.DataFrame, operations: List[str], **kwargs) -> pd.DataFrame:
        """
        데이터 클리닝 작업 수행
        
        Args:
            df: 처리할 DataFrame
            operations: 수행할 작업 리스트 ['remove_duplicates', 'fill_na', 'drop_na', 'reset_index']
            **kwargs: 작업별 추가 옵션
            
        Returns:
            처리된 DataFrame
        """
        try:
            result_df = df.copy()
            
            for operation in operations:
                if operation == 'remove_duplicates':
                    result_df = result_df.drop_duplicates(**kwargs.get('duplicate_options', {}))
                elif operation == 'fill_na':
                    result_df = result_df.fillna(kwargs.get('fill_value', 0))
                elif operation == 'drop_na':
                    result_df = result_df.dropna(**kwargs.get('dropna_options', {}))
                elif operation == 'reset_index':
                    result_df = result_df.reset_index(drop=kwargs.get('drop_index', True))
                    
            return result_df
        except Exception as e:
            self.logger.error(f"데이터 클리닝 중 오류 발생: {str(e)}")
            raise
            
    def data_transformation(self, df: pd.DataFrame, columns: List[str], operation: str, **kwargs) -> pd.DataFrame:
        """
        데이터 변환 작업 수행
        
        Args:
            df: 변환할 DataFrame
            columns: 변환할 열 리스트
            operation: 변환 작업 ('normalize', 'standardize', 'encode_categorical', 'datetime_convert')
            **kwargs: 추가 변환 옵션
            
        Returns:
            변환된 DataFrame
        """
        try:
            result_df = df.copy()
            
            if operation == 'normalize':
                for col in columns:
                    result_df[col] = (result_df[col] - result_df[col].min()) / (result_df[col].max() - result_df[col].min())
            elif operation == 'standardize':
                for col in columns:
                    result_df[col] = (result_df[col] - result_df[col].mean()) / result_df[col].std()
            elif operation == 'encode_categorical':
                for col in columns:
                    result_df[col] = pd.Categorical(result_df[col]).codes
            elif operation == 'datetime_convert':
                for col in columns:
                    result_df[col] = pd.to_datetime(result_df[col], **kwargs.get('datetime_options', {}))
                    
            return result_df
        except Exception as e:
            self.logger.error(f"데이터 변환 중 오류 발생: {str(e)}")
            raise
            
    def data_analysis(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict:
        """
        기본적인 데이터 분석 수행
        
        Args:
            df: 분석할 DataFrame
            columns: 분석할 열 리스트 (None인 경우 모든 수치형 열)
            
        Returns:
            분석 결과를 담은 딕셔너리
        """
        try:
            if columns is None:
                columns = df.select_dtypes(include=[np.number]).columns
                
            analysis_results = {
                'basic_stats': df[columns].describe(),
                'correlation': df[columns].corr(),
                'missing_values': df[columns].isnull().sum(),
                'unique_values': {col: df[col].nunique() for col in columns}
            }
            
            return analysis_results
        except Exception as e:
            self.logger.error(f"데이터 분석 중 오류 발생: {str(e)}")
            raise
            
    def data_grouping(self, df: pd.DataFrame, group_by: Union[str, List[str]], 
                     agg_columns: Dict[str, List[str]]) -> pd.DataFrame:
        """
        데이터 그룹화 및 집계 수행
        
        Args:
            df: 그룹화할 DataFrame
            group_by: 그룹화 기준 열
            agg_columns: 집계할 열과 집계 함수 (예: {'column1': ['mean', 'sum']})
            
        Returns:
            그룹화된 DataFrame
        """
        try:
            return df.groupby(group_by).agg(agg_columns)
        except Exception as e:
            self.logger.error(f"데이터 그룹화 중 오류 발생: {str(e)}")
            raise
            
    def data_filtering(self, df: pd.DataFrame, conditions: Dict[str, Dict]) -> pd.DataFrame:
        """
        조건에 따른 데이터 필터링
        
        Args:
            df: 필터링할 DataFrame
            conditions: 필터링 조건 (예: {'column1': {'operator': '>', 'value': 10}})
            
        Returns:
            필터링된 DataFrame
        """
        try:
            result_df = df.copy()
            
            operators = {
                '>': lambda x, y: x > y,
                '<': lambda x, y: x < y,
                '>=': lambda x, y: x >= y,
                '<=': lambda x, y: x <= y,
                '==': lambda x, y: x == y,
                '!=': lambda x, y: x != y,
                'in': lambda x, y: x.isin(y),
                'not in': lambda x, y: ~x.isin(y)
            }
            
            for column, condition in conditions.items():
                operator = condition['operator']
                value = condition['value']
                
                if operator not in operators:
                    raise ValueError(f"지원하지 않는 연산자입니다: {operator}")
                    
                result_df = result_df[operators[operator](result_df[column], value)]
                
            return result_df
        except Exception as e:
            self.logger.error(f"데이터 필터링 중 오류 발생: {str(e)}")
            raise
