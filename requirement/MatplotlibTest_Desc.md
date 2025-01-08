##### Celery 프레임워크의 다양한 구성 요소와 기능을 테스트하는 포괄적인 단위 테스트 세트.

1. line_plot : 선 그래프 생성
2. scatter_plot : 산점도 생성
3. bar_plot : 막대 그래프 생성
4. histogram : 히스토그램 생성
5. box_plot : 박스 플롯 생성
6. heatmap : 히트맵 생성
7. pie_chart : 파이 차트 생성
8. time_series : 시계열 그래프 생성
9. correlation_matrix : 상관관계 행렬 시각화


##### 시각화 유틸리티 초기화
##### matplotlib에서 'seaborn'스타일 없다. 사용시 라이브러리 설치, 스타일 matplotlib에 등록.
##### viz = Visualization(style='seaborn', figsize=(12, 6))

viz = Visualization()   # PlotConfig내 Style, figsize 선 설정됨