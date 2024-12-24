##### Celery 프레임워크의 다양한 구성 요소와 기능을 테스트하는 포괄적인 단위 테스트 세트.

1. 로그 메시지 및 주석을 한국어로 번역
2. 변수명과 함수명은 원래의 영어 버전 유지
3. 코드의 로직과 구조는 완전히 동일하게 유지

##### 테스트 클래스들은 다음과 같은 기능을 검증함

1. TestRedisManager: Redis 작업 상태 관리 테스트
    - 작업 상태 설정 및 검색
    - 데이터 간섭 방지를 위해 별도의 테스트 데이터베이스 사용
2. TestTaskLogger: 로깅 기능 테스트
    - 작업 시작 이벤트 로깅
    - 작업 성공 이벤트 로깅
3. TestBaseTask: 기본 작업 클래스 테스트
    - 작업 완료 처리
    - 로깅 및 상태 추적
4. TestTaskScheduler: 작업 스케줄링 테스트
    - Crontab을 사용한 작업 스케줄링
    - 잘못된 스케줄 처리
5. TestTaskMonitor: 작업 모니터링 테스트
    - 작업 정보 검색
    - Redis와 상호작용
6. TestDecoratorFunctions: 유틸리티 데코레이터 테스트
    - 재시도 메커니즘
    - 성능 측정

##### 테스트 실행시

1. 필요한 의존성 설치: pip install redis celery
2. celery_framework.py가 같은 디렉토리에 있는지 확인
3. 테스트 스크립트 실행: python test_celery_framework.py
