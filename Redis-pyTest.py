from common import RedispyCm
from typing import Dict, Any

def example_usage():
    # 설정
    config = RedispyCm.RedisConfig(
        host='localhost',
        port=6379,
        db=0
    )

    # 프레임워크 초기화
    redis_framework = RedispyCm.RedisFramework(config)

    # 캐시 사용 예시
    @redis_framework.cache.cached(timeout=300)
    def get_user_data(user_id: int) -> Dict[str, Any]:
        # 실제로는 DB 조회 등의 작업 수행
        return {"user_id": user_id, "name": "Test User"}

    # 락 사용 예시
    with redis_framework.create_lock("my_lock").acquire_lock():
        # 크리티컬 섹션 작업 수행
        pass

    # 큐 사용 예시
    queue = redis_framework.create_queue("my_queue")
    queue.enqueue({"task": "process_data"})
    task = queue.dequeue()

    # 발행/구독 사용 예시
    def message_handler(message):
        print(f"Received: {message}")

    redis_framework.pubsub.subscribe("my_channel", message_handler)
    redis_framework.pubsub.publish("my_channel", {"event": "update"})

    # 속도 제한 사용 예시
    rate_limiter = redis_framework.create_rate_limiter("api_calls", 100, 3600)
    if rate_limiter.is_allowed("user_123"):
        # API 호출 처리
        pass

if __name__ == "__main__":
    example_usage()