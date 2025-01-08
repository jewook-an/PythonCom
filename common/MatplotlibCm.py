import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Optional, List, Tuple, Dict, Any, Union
from datetime import datetime
import io
import base64

class PlotConfig:
    """플롯 설정 클래스"""
    #DEFAULT_STYLE = 'seaborn' # Error : style must be one of white, dark, whitegrid, darkgrid, ticks
    DEFAULT_STYLE = 'darkgrid'
    DEFAULT_FIGSIZE = (10, 6)
    DEFAULT_DPI = 100
    DEFAULT_COLORS = sns.color_palette('husl', 8)   #['b', 'g', 'r', 'c', 'm', 'y', 'k']

class Visualization:
    """시각화 유틸리티 클래스"""

    def __init__(
        self,
        style: str = PlotConfig.DEFAULT_STYLE,
        figsize: Tuple[int, int] = PlotConfig.DEFAULT_FIGSIZE,
        dpi: int = PlotConfig.DEFAULT_DPI
    ):
        """
        시각화 유틸리티 초기화

        Args:
            style: matplotlib 스타일
            figsize: 그림 크기
            dpi: 해상도
        """
        # plt.style.use(style)
        sns.set_theme(style=style)  # seaborn 스타일 설정
        self.figsize = figsize
        self.dpi = dpi
        self.colors = PlotConfig.DEFAULT_COLORS

    def create_figure(self) -> Tuple[Figure, Axes]:
        """새로운 figure와 axes 생성"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        return fig, ax

    def line_plot(
        self,
        data: Union[pd.DataFrame, Dict[str, List]],
        x: str,
        y: Union[str, List[str]],
        title: str = '',
        xlabel: str = '',
        ylabel: str = '',
        legend: bool = True,
        grid: bool = True,
        style: Optional[str] = None
    ) -> Figure:
        """
        선 그래프 생성

        Args:
            data: 데이터프레임 또는 딕셔너리
            x: x축 컬럼명
            y: y축 컬럼명 또는 리스트
            title: 그래프 제목
            xlabel: x축 레이블
            ylabel: y축 레이블
            legend: 범례 표시 여부
            grid: 그리드 표시 여부
            style: 선 스타일
        """
        fig, ax = self.create_figure()

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        if isinstance(y, str):
            y = [y]

        for idx, col in enumerate(y):
            ax.plot(data[x], data[col], label=col, color=self.colors[idx],
                   linestyle=style if style else '-')

        self._customize_plot(ax, title, xlabel, ylabel, legend, grid)
        return fig

    def scatter_plot(
        self,
        data: Union[pd.DataFrame, Dict[str, List]],
        x: str,
        y: str,
        title: str = '',
        xlabel: str = '',
        ylabel: str = '',
        color: Optional[str] = None,
        size: Optional[List[float]] = None,
        alpha: float = 0.6
    ) -> Figure:
        """산점도 생성"""
        fig, ax = self.create_figure()

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        ax.scatter(data[x], data[y], c=color, s=size, alpha=alpha)
        self._customize_plot(ax, title, xlabel, ylabel)
        return fig

    def bar_plot(
        self,
        data: Union[pd.DataFrame, Dict[str, List]],
        x: str,
        y: str,
        title: str = '',
        xlabel: str = '',
        ylabel: str = '',
        orientation: str = 'vertical',
        color: Optional[str] = None
    ) -> Figure:
        """막대 그래프 생성"""
        fig, ax = self.create_figure()

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        if orientation == 'vertical':
            ax.bar(data[x], data[y], color=color if color else self.colors[0])
        else:
            ax.barh(data[x], data[y], color=color if color else self.colors[0])

        self._customize_plot(ax, title, xlabel, ylabel)
        return fig

    def histogram(
        self,
        data: Union[List, np.ndarray],
        bins: int = 30,
        title: str = '',
        xlabel: str = '',
        ylabel: str = 'Frequency',
        density: bool = False,
        color: Optional[str] = None
    ) -> Figure:
        """히스토그램 생성"""
        fig, ax = self.create_figure()

        ax.hist(data, bins=bins, density=density,
                color=color if color else self.colors[0], alpha=0.7)

        self._customize_plot(ax, title, xlabel, ylabel)
        return fig

    def box_plot(
        self,
        data: Union[pd.DataFrame, Dict[str, List]],
        x: Optional[str] = None,
        y: str = '',
        title: str = '',
        xlabel: str = '',
        ylabel: str = ''
    ) -> Figure:
        """박스 플롯 생성"""
        fig, ax = self.create_figure()

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        sns.boxplot(data=data, x=x, y=y, ax=ax)
        self._customize_plot(ax, title, xlabel, ylabel)
        return fig

    def heatmap(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        title: str = '',
        cmap: str = 'YlOrRd',
        annot: bool = True,
        fmt: str = '.2f'
    ) -> Figure:
        """히트맵 생성"""
        fig, ax = self.create_figure()

        if isinstance(data, pd.DataFrame):
            data_matrix = data
        else:
            data_matrix = pd.DataFrame(data)

        sns.heatmap(data_matrix, cmap=cmap, annot=annot, fmt=fmt, ax=ax)
        ax.set_title(title)
        plt.tight_layout()
        return fig

    def pie_chart(
        self,
        values: List[float],
        labels: List[str],
        title: str = '',
        autopct: str = '%1.1f%%',
        startangle: float = 90
    ) -> Figure:
        """파이 차트 생성"""
        fig, ax = self.create_figure()

        ax.pie(values, labels=labels, autopct=autopct, startangle=startangle,
               colors=self.colors)
        ax.axis('equal')
        ax.set_title(title)
        return fig

    def time_series(
        self,
        data: Union[pd.DataFrame, Dict[str, List]],
        date_column: str,
        value_columns: Union[str, List[str]],
        title: str = '',
        xlabel: str = 'Date',
        ylabel: str = '',
        date_format: str = '%Y-%m-%d'
    ) -> Figure:
        """시계열 그래프 생성"""
        fig, ax = self.create_figure()

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        if isinstance(value_columns, str):
            value_columns = [value_columns]

        data[date_column] = pd.to_datetime(data[date_column])

        for idx, col in enumerate(value_columns):
            ax.plot(data[date_column], data[col], label=col,
                   color=self.colors[idx])

        ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        plt.xticks(rotation=45)

        self._customize_plot(ax, title, xlabel, ylabel, legend=True, grid=True)
        return fig

    def correlation_matrix(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        title: str = 'Correlation Matrix'
    ) -> Figure:
        """상관관계 행렬 시각화"""
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)

        corr_matrix = data.corr()

        fig, ax = self.create_figure()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1,
                   center=0, ax=ax)
        ax.set_title(title)
        plt.tight_layout()
        return fig

    def _customize_plot(
        self,
        ax: Axes,
        title: str,
        xlabel: str,
        ylabel: str,
        legend: bool = False,
        grid: bool = False
    ) -> None:
        """플롯 커스터마이징"""
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if legend:
            ax.legend()
        if grid:
            ax.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

    def save_plot(
        self,
        fig: Figure,
        filename: str,
        format: str = 'png',
        dpi: Optional[int] = None
    ) -> None:
        """플롯 저장"""
        fig.savefig(filename, format=format, dpi=dpi if dpi else self.dpi,
                   bbox_inches='tight')

    def get_plot_base64(
        self,
        fig: Figure,
        format: str = 'png'
    ) -> str:
        """플롯을 base64 인코딩된 문자열로 변환"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format=format, bbox_inches='tight')
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode()

    def show_plot(self, fig):
        """그래프를 화면에 표시합니다."""
        plt.show()

    def close_plot(self, fig: Figure) -> None:
        """플롯 메모리 해제"""
        plt.close(fig)

# 사용 예시
"""
# 시각화 유틸리티 초기화
viz = Visualization(style='seaborn', figsize=(12, 6))

# 샘플 데이터
data = {
    'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'value1': np.random.randn(100).cumsum(),
    'value2': np.random.randn(100).cumsum()
}

# 시계열 그래프 생성
fig = viz.time_series(
    data=data,
    date_column='date',
    value_columns=['value1', 'value2'],
    title='Time Series Example',
    ylabel='Value'
)

# 플롯 저장
viz.save_plot(fig, 'time_series.png')
viz.close_plot(fig)

# 산점도 생성
scatter_data = {
    'x': np.random.randn(100),
    'y': np.random.randn(100)
}

fig = viz.scatter_plot(
    data=scatter_data,
    x='x',
    y='y',
    title='Scatter Plot Example'
)

# base64 인코딩
base64_str = viz.get_plot_base64(fig)
viz.close_plot(fig)
"""
