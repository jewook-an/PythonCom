from common import Visualization
"""
line_plot : 선 그래프 생성
scatter_plot : 산점도 생성
bar_plot : 막대 그래프 생성
histogram : 히스토그램 생성
box_plot : 박스 플롯 생성
heatmap : 히트맵 생성
pie_chart : 파이 차트 생성
time_series : 시계열 그래프 생성
correlation_matrix : 상관관계 행렬 시각화
_customize_plot : 플롯 커스터마이징
"""
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

########################################################################
# 시계열 그래프 생성
########################################################################
fig = viz.time_series(
    data=data,
    date_column='date',
    value_columns=['value1', 'value2'],
    title='Time Series Example',
    ylabel='Value'
)

# 플롯 저장
viz.save_plot(fig, 'time_series.png')

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)

########################################################################
# 산점도 생성
########################################################################
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

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)

########################################################################
# 선 그래프 생성
########################################################################
line_data = {
    'x': np.arange(10),
    'y1': np.random.rand(10),
    'y2': np.random.rand(10)
}

fig = viz.line_plot(
    data=line_data,
    x='x',
    y=['y1', 'y2'],
    title='Line Plot Example'
)

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)

########################################################################
# 막대 그래프 생성
########################################################################
bar_data = {
    'categories': ['A', 'B', 'C', 'D'],
    'values': [3, 7, 5, 9]
}

fig = viz.bar_plot(
    data=bar_data,
    x='categories',
    y='values',
    title='Bar Plot Example'
)

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)

########################################################################
# 히스토그램 생성
########################################################################
hist_data = np.random.randn(1000)

fig = viz.histogram(
    data=hist_data,
    bins=30,
    title='Histogram Example'
)

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)

########################################################################
# 박스 플롯 생성
########################################################################
box_data = {
    'group': ['A'] * 50 + ['B'] * 50,
    'values': np.random.randn(100)
}

fig = viz.box_plot(
    data=box_data,
    x='group',
    y='values',
    title='Box Plot Example'
)

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)

########################################################################
# 히트맵 생성
########################################################################
heatmap_data = np.random.rand(10, 10)

fig = viz.heatmap(
    data=heatmap_data,
    title='Heatmap Example'
)

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)

########################################################################
# 파이 차트 생성
########################################################################
pie_values = [15, 30, 45, 10]
pie_labels = ['Category A', 'Category B', 'Category C', 'Category D']

fig = viz.pie_chart(
    values=pie_values,
    labels=pie_labels,
    title='Pie Chart Example'
)

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)
########################################################################
# 상관관계 행렬 시각화
########################################################################
corr_data = np.random.rand(10, 10)

fig = viz.correlation_matrix(
    data=corr_data,
    title='Correlation Matrix Example'
)

# 플롯 화면에 표시
viz.show_plot(fig)

# 플롯 닫기
viz.close_plot(fig)
