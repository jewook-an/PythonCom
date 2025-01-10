from common import RedispyCm
"""
from PythonCom.common import RedispyCm
>> pytest filename.py : 정상    >> 2 Warning
>> python filename.py : 에러    >> No module named 'PythonCom'

from common import RedispyCm
>> pytest filename.py : 에러    >> No module named 'common'
>> python filename.py : 정상
"""
# Redis의 다양한 기능 활용 데이터 캐싱, 동시성 제어, 메시징, 작업 큐, API 호출 제한 등을 구현하는 방법을 보여줌.

from typing import Dict, Any

def example_usage():
    # 설정
    config = RedispyCm.RedisConfig(
        host='localhost',
        port=6379,
        db=0    # 기본 데이터베이스(0번)를 지정
    )

    # 프레임워크 초기화
    redis_framework = RedispyCm.RedisFramework(config)

    # 캐시 사용 예시
    @redis_framework.cache.cached(timeout=300)          # 사용자 ID > 사용자 데이터 반환. Redis캐시 사용, 300초 동안 결과를 저장
    def get_user_data(user_id: int) -> Dict[str, Any]:
        # 실제로는 DB 조회 등의 작업 수행
        return {"user_id": user_id, "name": "Test User"}

    # 락 사용 예시 : my_lock 이름의 락 생성, 이를 사용해 크리티컬 섹션 보호. 실제 작업이 수행되지 않지만, 락을 통한 동시성 문제를 방지할 수 있다.
    with redis_framework.create_lock("my_lock").acquire_lock():
        # 크리티컬 섹션 작업 수행
        pass

    # 큐 사용 예시 : my_queue 이름의 큐 생성, 작업을 큐에 추가후, 큐에서 작업을 꺼내는 예시.
    queue = redis_framework.create_queue("my_queue")
    queue.enqueue({"task": "process_data"})
    task = queue.dequeue()

    # 발행/구독 사용 예시
    # my_channel 채널에 메시지를 구독, 메시지 수신시 message_handler 함수 호출됨. 또, 해당 채널에 메시지 발행 예시도 포함돼 있음.
    def message_handler(message):
        print(f"Received: {message}")

    redis_framework.pubsub.subscribe("my_channel", message_handler)
    redis_framework.pubsub.publish("my_channel", {"event": "update"})

    # 속도 제한 사용 예시
    # api_calls 이름의 속도 제한기 생성, 1시간에 100번 호출 허용. 특정 사용자의 호출여부 확인 예시.
    rate_limiter = redis_framework.create_rate_limiter("api_calls", 100, 3600)
    if rate_limiter.is_allowed("user_123"):
        # API 호출 처리
        pass

# 스크립트 직접 실행시 example_usage 함수 호출해 위의 모든 예시 실행.
if __name__ == "__main__":
    example_usage()