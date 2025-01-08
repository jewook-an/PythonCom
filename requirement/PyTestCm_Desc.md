#### 기본 설정 및 로깅 설정
class TestConfig:

#### 공통 페이지 객체 (Page Object Model)
class BasePage
    - log_step(self, step_name: str, details: str = ""):
    - verify_element_present(self, element: str) -> bool:

#### 테스트 데이터 관리
class TestDataManager
    - load_data(self) -> Dict[str, Any]:
    - get_test_data(self, test_case: str) -> Dict[str, Any]:

#### 공통 테스트 픽스처
    - test_config():
    - test_data_manager():
    - setup_teardown(request):

##### 커스텀 마커 정의
    - pytest_configure(config):

##### 테스트 결과 리포터
class CustomReporter
    - pytest_runtest_makereport(item, call):

#### 샘플 테스트 케이스
class TestExample
    - test_login(self, test_config, test_data_manager):
    - test_user_access(self, user_type, test_config):

#### 유틸리티 함수
class TestUtils:
    """조건이 만족될 때까지 대기하는 유틸리티 함수"""
    - wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5):
    """스크린샷 캡처 유틸리티"""
    - capture_screenshot(driver, name: str):
