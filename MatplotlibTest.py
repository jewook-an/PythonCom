from common import Visualization
import pandas as pd
import numpy as np

# 시각화 유틸리티 초기화
# matplotlib에서 'seaborn'스타일 없다. 사용시 라이브러리 설치, 스타일 matplotlib에 등록.
# viz = Visualization(style='seaborn', figsize=(12, 6))
viz = Visualization()   # PlotConfig내 Style, figsize 선 설정됨

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
