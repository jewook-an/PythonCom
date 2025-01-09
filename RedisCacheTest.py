import redis
import time

# Redis 클라이언트 설정
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=15, password='redisPass', decode_responses=True)

def get_data_from_cache(key):
    """
    Redis에서 데이터를 가져옵니다.
    """
    value = redis_client.get(key)
    if value:
        print(f"Cache hit: {value}")
    else:
        print("Cache miss")
    return value

def set_data_to_cache(key, value, ttl=60):
    """
    Redis에 데이터를 저장합니다.
    """
    redis_client.set(key, value, ex=ttl)
    print(f"Data cached: {key} -> {value} (TTL: {ttl} seconds)")

def expensive_operation():
    """
    오래 걸리는 작업(예: 외부 API 호출 시뮬레이션).
    """
    print("Performing an expensive operation...")
    time.sleep(2)
    return "Expensive result"

# 메인 로직
def main():
    cache_key = "expensive_data"

    # 캐시에서 데이터 가져오기
    cached_data = get_data_from_cache(cache_key)

    if not cached_data:
        # 캐시된 데이터가 없으면 작업 실행
        result = expensive_operation()

        # 결과를 Redis에 저장
        set_data_to_cache(cache_key, result)

        print(f"Fresh data: {result}")
    else:
        print(f"Cached data: {cached_data}")

if __name__ == "__main__":
    main()
