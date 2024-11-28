import redis
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime, timedelta
import json
import pickle
import hashlib
import logging
import time
from functools import wraps
from contextlib import contextmanager
import threading
from dataclasses import dataclass

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='redis_operations.log'
)
logger = logging.getLogger(__name__)

@dataclass
class RedisConfig:
    """Redis 설정 클래스"""
    host: str = 'localhost'
    port: int = 6379
    db: int = 0
    decode_responses: bool = True
    socket_timeout: int = 5
    retry_on_timeout: bool = True
    max_connections: int = 10
    password: Optional[str] = None

class RedisConnectionPool:
    """Redis 연결 풀 관리"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, config: RedisConfig):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.pool = redis.ConnectionPool(
                    host=config.host,
                    port=config.port,
                    db=config.db,
                    decode_responses=config.decode_responses,
                    password=config.password,
                    max_connections=config.max_connections
                )
        return cls._instance

    def get_connection(self) -> redis.Redis:
        return redis.Redis(connection_pool=self.pool)

class RedisCache:
    """캐시 관리 클래스"""
    def __init__(self, config: RedisConfig):
        self.connection_pool = RedisConnectionPool(config)
        self.client = self.connection_pool.get_connection()

    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        """캐시 키 생성"""
        key_parts = [prefix]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        key = ":".join(key_parts)
        return hashlib.md5(key.encode()).hexdigest()

    def cached(self, timeout: int = 300):
        """캐시 데코레이터"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self.cache_key(func.__name__, *args, **kwargs)
                result = self.client.get(cache_key)

                if result is not None:
                    return pickle.loads(result)

                result = func(*args, **kwargs)
                self.client.setex(
                    cache_key,
                    timeout,
                    pickle.dumps(result)
                )
                return result
            return wrapper
        return decorator

class RedisLock:
    """분산 락 관리"""
    def __init__(self, redis_client: redis.Redis, lock_name: str, timeout: int = 10):
        self.redis_client = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.lock_token = hashlib.md5(str(time.time()).encode()).hexdigest()

    @contextmanager
    def acquire_lock(self, blocking: bool = True, retry_delay: float = 0.1):
        acquired = False
        try:
            while not acquired:
                acquired = self.redis_client.set(
                    self.lock_name,
                    self.lock_token,
                    nx=True,
                    ex=self.timeout
                )
                if acquired:
                    yield True
                    break
                if not blocking:
                    yield False
                    break
                time.sleep(retry_delay)
        finally:
            if acquired:
                self.release_lock()

    def release_lock(self):
        """락 해제"""
        if self.redis_client.get(self.lock_name) == self.lock_token:
            self.redis_client.delete(self.lock_name)

class RedisQueue:
    """큐 관리"""
    def __init__(self, redis_client: redis.Redis, queue_name: str):
        self.redis_client = redis_client
        self.queue_name = f"queue:{queue_name}"

    def enqueue(self, item: Any):
        """큐에 항목 추가"""
        self.redis_client.rpush(self.queue_name, pickle.dumps(item))

    def dequeue(self, timeout: int = 0) -> Optional[Any]:
        """큐에서 항목 제거 및 반환"""
        result = self.redis_client.blpop(self.queue_name, timeout=timeout)
        if result:
            return pickle.loads(result[1])
        return None

    def size(self) -> int:
        """큐 크기 반환"""
        return self.redis_client.llen(self.queue_name)

class RedisPubSub:
    """발행/구독 관리"""
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.pubsub = self.redis_client.pubsub()

    def publish(self, channel: str, message: Any):
        """메시지 발행"""
        self.redis_client.publish(channel, pickle.dumps(message))

    def subscribe(self, channel: str, callback: Callable[[Any], None]):
        """채널 구독"""
        self.pubsub.subscribe(**{channel: lambda message:
            callback(pickle.loads(message['data'])) if message['type'] == 'message' else None})

    def start_listening(self):
        """메시지 수신 시작"""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                yield pickle.loads(message['data'])

class RedisRateLimiter:
    """속도 제한 관리"""
    def __init__(self, redis_client: redis.Redis, key_prefix: str, limit: int, window: int):
        self.redis_client = redis_client
        self.key_prefix = key_prefix
        self.limit = limit
        self.window = window

    def is_allowed(self, identifier: str) -> bool:
        """요청 허용 여부 확인"""
        key = f"{self.key_prefix}:{identifier}"
        current = self.redis_client.get(key)

        if not current:
            self.redis_client.setex(key, self.window, 1)
            return True

        if int(current) >= self.limit:
            return False

        self.redis_client.incr(key)
        return True

class RedisDataManager:
    """데이터 관리"""
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def set_data(self, key: str, value: Any, expire: Optional[int] = None):
        """데이터 저장"""
        serialized = pickle.dumps(value)
        if expire:
            self.redis_client.setex(key, expire, serialized)
        else:
            self.redis_client.set(key, serialized)

    def get_data(self, key: str) -> Optional[Any]:
        """데이터 조회"""
        data = self.redis_client.get(key)
        return pickle.loads(data) if data else None

    def increment(self, key: str, amount: int = 1) -> int:
        """증가"""
        return self.redis_client.incrby(key, amount)

    def expire_at(self, key: str, timestamp: datetime):
        """만료 시간 설정"""
        self.redis_client.expireat(key, int(timestamp.timestamp()))

class RedisHealthCheck:
    """헬스 체크"""
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def check_connection(self) -> bool:
        """연결 상태 확인"""
        try:
            return self.redis_client.ping()
        except redis.ConnectionError:
            return False

    def get_info(self) -> Dict[str, Any]:
        """Redis 서버 정보 조회"""
        return self.redis_client.info()

class RedisFramework:
    """통합 Redis 프레임워크"""
    def __init__(self, config: RedisConfig):
        self.config = config
        self.client = RedisConnectionPool(config).get_connection()

        # 각 기능 초기화
        self.cache = RedisCache(config)
        self.data_manager = RedisDataManager(self.client)
        self.pubsub = RedisPubSub(self.client)
        self.health_check = RedisHealthCheck(self.client)

    def create_lock(self, lock_name: str, timeout: int = 10) -> RedisLock:
        """락 생성"""
        return RedisLock(self.client, lock_name, timeout)

    def create_queue(self, queue_name: str) -> RedisQueue:
        """큐 생성"""
        return RedisQueue(self.client, queue_name)

    def create_rate_limiter(self, key_prefix: str, limit: int, window: int) -> RedisRateLimiter:
        """속도 제한기 생성"""
        return RedisRateLimiter(self.client, key_prefix, limit, window)

"""
# 사용 예시
def example_usage():
    # 설정
    config = RedisConfig(
        host='localhost',
        port=6379,
        db=0
    )

    # 프레임워크 초기화
    redis_framework = RedisFramework(config)

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
"""