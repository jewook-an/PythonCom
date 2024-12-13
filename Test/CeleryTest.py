import unittest
import time
import json
import redis
from unittest.mock import patch, MagicMock
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

# 원본 모듈 가져오기
#from common import CeleryCm as cf # 타 경로에 있는 부분 Common 모듈 가져오지 못함
from PythonCom.common import CeleryCm as cf

class TestRedisManager(unittest.TestCase):
    def setUp(self):
        # 프로덕션 데이터에 방해되지 않도록 테스트 데이터베이스 사용
        self.redis_manager = cf.RedisManager(db=15)

    def test_set_and_get_task_status(self):
        task_id = 'test_task_123'
        status = {
            'status': 'RUNNING',
            'started_at': str(time.time())
        }

        # 작업 상태 설정
        self.redis_manager.set_task_status(task_id, status)

        # 작업 상태 검색
        retrieved_status = self.redis_manager.get_task_status(task_id)

        # 검색된 상태가 설정된 상태와 일치하는지 확인
        self.assertEqual(retrieved_status['status'], 'RUNNING')
        self.assertTrue('started_at' in retrieved_status)

    def tearDown(self):
        # 테스트 데이터베이스 초기화
        self.redis_manager.redis_client.flushdb()

class TestTaskLogger(unittest.TestCase):
    def setUp(self):
        self.task_logger = cf.TaskLogger('test_logger')

    @patch('logging.Logger.info')
    def test_log_task_start(self, mock_log_info):
        task_id = 'test_task_start'
        args = (1, 2)
        kwargs = {'x': 3}

        self.task_logger.log_task_start(task_id, args, kwargs)

        mock_log_info.assert_called_once_with(
            f"작업 {task_id} 시작: 인자: {args}, 키워드 인자: {kwargs}"
        )

    @patch('logging.Logger.info')
    def test_log_task_success(self, mock_log_info):
        task_id = 'test_task_success'
        result = 42

        self.task_logger.log_task_success(task_id, result)

        mock_log_info.assert_called_once_with(
            f"작업 {task_id} 성공적으로 완료: 결과: {result}"
        )

class TestBaseTask(unittest.TestCase):
    def setUp(self):
        self.base_task = cf.BaseTask()
        self.base_task.name = 'test_base_task'

    @patch('celery_framework.RedisManager.set_task_status')
    @patch('celery_framework.TaskLogger.log_task_success')
    def test_on_success(self, mock_log_success, mock_set_task_status):
        task_id = 'test_success_task'
        retval = {'result': 'success'}
        args = (1, 2)
        kwargs = {'x': 3}

        self.base_task.on_success(retval, task_id, args, kwargs)

        mock_log_success.assert_called_once()
        mock_set_task_status.assert_called_once_with(
            task_id,
            {
                'status': 'SUCCESS',
                'result': json.dumps(retval)
            }
        )

class TestTaskScheduler(unittest.TestCase):
    def setUp(self):
        self.app = Celery('test_tasks')
        self.scheduler = cf.TaskScheduler(self.app)

    def test_schedule_task_with_crontab(self):
        mock_task = MagicMock()
        mock_task.name = 'test_periodic_task'

        schedule = {
            'crontab': {
                'minute': '0',
                'hour': '*'
            }
        }

        self.scheduler.schedule_task(mock_task, schedule, 'hourly_task')

        self.assertIn('hourly_task', self.app.conf.beat_schedule)
        scheduled_task = self.app.conf.beat_schedule['hourly_task']

        self.assertEqual(scheduled_task['task'], mock_task.name)
        self.assertEqual(scheduled_task['args'], ())
        self.assertEqual(scheduled_task['kwargs'], {})

    def test_schedule_task_invalid_schedule(self):
        mock_task = MagicMock()
        mock_task.name = 'test_task'

        with self.assertRaises(ValueError):
            self.scheduler.schedule_task(mock_task, {'invalid': 'schedule'})

class TestTaskMonitor(unittest.TestCase):
    def setUp(self):
        self.redis_manager = cf.RedisManager(db=15)
        self.task_monitor = cf.TaskMonitor(self.redis_manager)

    def test_get_task_info(self):
        task_id = 'test_task_monitor'
        status = {
            'status': 'RUNNING',
            'start_time': str(time.time())
        }

        self.redis_manager.set_task_status(task_id, status)

        task_info = self.task_monitor.get_task_info(task_id)

        self.assertEqual(task_info['status'], 'RUNNING')
        self.assertTrue('start_time' in task_info)

    def tearDown(self):
        self.redis_manager.redis_client.flushdb()

class TestDecoratorFunctions(unittest.TestCase):
    def test_retry_on_failure(self):
        @cf.retry_on_failure(max_retries=3, delay=0.1)
        def flaky_function(fail_count=[0]):
            fail_count[0] += 1
            if fail_count[0] < 3:
                raise Exception("시뮬레이션된 실패")
            return "성공"

        result = flaky_function()
        self.assertEqual(result, "성공")

    @patch('logging.info')
    def test_measure_performance(self, mock_log_info):
        @cf.measure_performance
        def sample_function(x, y):
            time.sleep(0.1)  # 작업 시뮬레이션
            return x + y

        result = sample_function(10, 20)

        self.assertEqual(result, 30)
        mock_log_info.assert_called_once()
        self.assertTrue("sample_function" in mock_log_info.call_args[0][0])

def main():
    unittest.main()

if __name__ == '__main__':
    main()


"""
# 사용 예시
if __name__ == '__main__':
    # 작업 실행
    result = sample_task.delay(10, 20)

    # 작업 모니터링
    monitor = TaskMonitor(RedisManager())
    task_status = monitor.get_task_info(result.id)

    print(f"Task status: {task_status}")

# 새로운 작업 정의
@app.task(base=BaseTask, bind=True)
@measure_performance
@retry_on_failure(max_retries=3)
def process_data(self, data):
    with task_error_handler():
        # 데이터 처리 로직
        result = perform_processing(data)
        return result

# 주기적 작업 설정
scheduler.schedule_task(
    process_data,
    {
        'interval': {
            'hours': 1
        }
    },
    'hourly_processing'
)

# 작업 실행
result = process_data.delay(some_data)

# 상태 확인
monitor = TaskMonitor(RedisManager())
status = monitor.get_task_info(result.id)
"""

"""
# Celery 워커 시작
celery -A tasks worker --loglevel=info

# Celery Beat 시작 (주기적 작업용)
celery -A tasks beat --loglevel=info
"""