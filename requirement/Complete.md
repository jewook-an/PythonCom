#### TEST 완료 모듈

1. NumPy (완료)
2. Pandas (완료 및 추가)
3. Requests (완료)
4. SQLAlchemy (완료)
    - MongoDB 연결 테스트
        * 필요항목 : 각각 Model 만들기
    - PostgreSQL 연결 테스트
        * 필요항목 : 각각 Model 만들기
5. FastAPI (진행중)
    -
6. Matplotlib (완료)
    - line_plot : 선 그래프 생성
    - scatter_plot : 산점도 생성
    - bar_plot : 막대 그래프 생성
    - histogram : 히스토그램 생성
    - box_plot : 박스 플롯 생성
    - heatmap : 히트맵 생성
    - pie_chart : 파이 차트 생성
    - time_series : 시계열 그래프 생성
    - correlation_matrix : 상관관계 행렬 시각화

7. PyTest (완료)
    - common/calculator.py : calculator 참조
    - Test/PytestTest.py : 실행 Test (11개 Test module)
8. Celery (완료)
    - Redis Server 생성, Test

9. Redis-py (완료)
    - RedisCacheTest.py     : Redis Cache Test
    - Redis-pyTest.py
        - 캐시 사용 예시 : 사용자 ID > 사용자 데이터 반환. Redis캐시 사용, 300초 동안 결과를 저장
        - 락 사용 예시 : my_lock 이름의 락 생성, 이를 사용해 크리티컬 섹션 보호. 실제 작업이 수행되지 않지만, 락을 통한 동시성 문제를 방지할 수 있다.
        - 큐 사용 예시 : my_queue 이름의 큐 생성, 작업을 큐에 추가후, 큐에서 작업을 꺼내는 예시.
        - 발행/구독 사용 예시 : my_channel 채널에 메시지를 구독, 메시지 수신시 message_handler 함수 호출됨. 또, 해당 채널에 메시지 발행 예시도 포함돼 있음.
        - 속도 제한 사용 예시 : api_calls 이름의 속도 제한기 생성, 1시간에 100번 호출 허용. 특정 사용자의 호출여부 확인 예시.

10.Pillow (PIL) (진행중)
<!--
-->

## 별도 TEST
1. APT TEST
    - python Test/co2_emission.py
    - python Test/covid_stats_via_xpath.py

2. 구글 Crawling 테스트
    - 구글검색 : python Test/crawl_google_results.py python programming
    - 학술자료 인용 Get : crawl_google_scholar_citation.py (제목,출판연도,저널의권,페이지)