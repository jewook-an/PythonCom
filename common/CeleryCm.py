from celery import Celery, Task
from celery.schedules import crontab
from celery.signals import after_task_publish, task_prerun, task_success, task_failure
from datetime import timedelta
import logging
import redis
import json
from typing import Any, Dict, Optional
from contextlib import contextmanager
import time
from functools import wraps

# 기본 설정
class CeleryConfig:
    # Celery 브로커 및 백엔드 설정
    BROKER_URL = 'redis://localhost:6379/0'
    RESULT_BACKEND = 'redis://localhost:6379/1'
    
    # 작업 설정
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Seoul'
    CELERY_ENABLE_UTC = True
    
    # 작업 제한 설정
    CELERY_TASK_SOFT_TIME_LIMIT = 600  # 10분
    CELERY_TASK_TIME_LIMIT = 1200      # 20분
    CELERY_TASK_MAX_RETRIES = 3
    
    # 동시성 설정
    CELERYD_CONCURRENCY = 4
    CELERYD_PREFETCH_MULTIPLIER = 1

# Celery 앱 초기화
app = Celery('tasks')
app.config_from_object(CeleryConfig)

# Redis 연결 관리
class RedisManager:
    def __init__(self, host='localhost', port=6379, db=2):
        self.redis_client = redis.Redis(host=host, port=port, db=db)
    
    def set_task_status(self, task_id: str, status: Dict[str, Any]):
        self.redis_client.hset(f"task_status:{task_id}", mapping=status)
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        return {k.decode(): v.decode() for k, v in self.redis_client.hgetall(f"task_status:{task_id}").items()}

# 로깅 설정
class TaskLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 파일 핸들러 추가
        handler = logging.FileHandler(f'celery_tasks_{name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_task_start(self, task_id: str, args: tuple, kwargs: dict):
        self.logger.info(f"Task {task_id} started with args: {args}, kwargs: {kwargs}")
    
    def log_task_success(self, task_id: str, result: Any):
        self.logger.info(f"Task {task_id} completed successfully with result: {result}")
    
    def log_task_failure(self, task_id: str, exc: Exception, traceback: str):
        self.logger.error(f"Task {task_id} failed: {exc}\n{traceback}")

# 기본 작업 클래스
class BaseTask(Task):
    abstract = True
    
    def __init__(self):
        self.logger = TaskLogger(self.name)
        self.redis_manager = RedisManager()
    
    def on_success(self, retval, task_id, args, kwargs):
        self.logger.log_task_success(task_id, retval)
        self.redis_manager.set_task_status(task_id, {
            'status': 'SUCCESS',
            'result': json.dumps(retval) if retval is not None else None
        })
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.logger.log_task_failure(task_id, exc, einfo.traceback)
        self.redis_manager.set_task_status(task_id, {
            'status': 'FAILURE',
            'error': str(exc)
        })

# 재시도 데코레이터
def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

# 성능 측정 데코레이터
def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logging.info(f"Task {func.__name__} took {duration:.2f} seconds to complete")
        return result
    return wrapper

# 주기적 작업 스케줄러
class TaskScheduler:
    def __init__(self, app: Celery):
        self.app = app
    
    def schedule_task(self, task, schedule: Dict[str, Any], name: Optional[str] = None):
        self.app.conf.beat_schedule[name or task.name] = {
            'task': task.name,
            'schedule': self._parse_schedule(schedule),
            'args': schedule.get('args', ()),
            'kwargs': schedule.get('kwargs', {})
        }
    
    def _parse_schedule(self, schedule: Dict[str, Any]) -> Any:
        if 'crontab' in schedule:
            return crontab(**schedule['crontab'])
        elif 'interval' in schedule:
            return timedelta(**schedule['interval'])
        else:
            raise ValueError("Invalid schedule format")

# 작업 모니터링
class TaskMonitor:
    def __init__(self, redis_manager: RedisManager):
        self.redis_manager = redis_manager
    
    def get_task_info(self, task_id: str) -> Dict[str, Any]:
        return self.redis_manager.get_task_status(task_id)
    
    def get_active_tasks(self) -> List[str]:
        return [k.decode().split(':')[1] for k in 
                self.redis_manager.redis_client.keys('task_status:*')]

# 샘플 작업 정의
@app.task(base=BaseTask, bind=True)
@measure_performance
@retry_on_failure(max_retries=3)
def sample_task(self, x: int, y: int) -> int:
    """샘플 계산 작업"""
    return x + y

@app.task(base=BaseTask, bind=True)
def periodic_task(self):
    """주기적으로 실행되는 작업"""
    self.logger.logger.info("Periodic task executed")

# 작업 스케줄 설정 예시
scheduler = TaskScheduler(app)
scheduler.schedule_task(
    periodic_task,
    {
        'crontab': {
            'minute': '0',
            'hour': '*'
        }
    },
    'hourly_task'
)

# 에러 처리
@contextmanager
def task_error_handler():
    try:
        yield
    except Exception as e:
        logging.error(f"Task error: {str(e)}")
        raise

# Celery 시그널 핸들러
@after_task_publish.connect
def task_sent_handler(sender=None, headers=None, **kwargs):
    logging.info(f"Task {sender} sent for processing")

@task_prerun.connect
def task_prerun_handler(task_id=None, task=None, **kwargs):
    logging.info(f"Task {task.name}[{task_id}] is about to run")

@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    logging.info(f"Task {sender.name} completed successfully with result: {result}")

@task_failure.connect
def task_failure_handler(sender=None, exception=None, **kwargs):
    logging.error(f"Task {sender.name} failed: {str(exception)}")

# 사용 예시
if __name__ == '__main__':
    # 작업 실행
    result = sample_task.delay(10, 20)
    
    # 작업 모니터링
    monitor = TaskMonitor(RedisManager())
    task_status = monitor.get_task_info(result.id)
    
    print(f"Task status: {task_status}")
