"""
pytest 를 이용한 Test Case : Error

# 해결 필요
FAILED FastAPITest.py::test_create_user - assert 404 == 201
FAILED FastAPITest.py::test_get_user - assert 404 == 200
FAILED FastAPITest.py::test_update_user - assert 404 == 200
FAILED FastAPITest.py::test_delete_user - assert 404 == 204

Command:
pytest FastAPITest.py

"""
import pytest
from fastapi.testclient import TestClient
from .common.FastapiCm import AppFactory, DatabaseConfig

# 애플리케이션과 데이터베이스 초기화
app, db = AppFactory.create_app(
    title="Test FastAPI App",
    db_config=DatabaseConfig(db_url="postgresql://postgres:godlast@localhost:5432/postgres")
)

# TestClient를 사용해 FastAPI 앱 테스트
client = TestClient(app)

@app.get("/")
async def read_root():
    return {"message": "FastAPI App is running!"}

@pytest.fixture(scope="module")
def db_session():
    """데이터베이스 세션을 제공하는 테스트용 의존성"""
    with db.get_db() as session:
        yield session

def test_app_health_check():
    """애플리케이션이 제대로 실행되는지 확인"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI App is running!"}

def test_create_user(db_session):
    """사용자 생성 테스트"""
    # 테스트 데이터
    test_data = {
        "username": "test_user3",
        "email": "test_user3@example.com"
    }
    response = client.post("/users/", json=test_data)
    assert response.status_code == 201
    assert response.json()["email"] == test_data["email"]

def test_get_user(db_session):
    """사용자 정보 가져오기 테스트"""
    user_id = 1  # 예시 ID
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_update_user(db_session):
    """사용자 정보 업데이트 테스트"""
    user_id = 1
    update_data = {
        "email": "updated_user@example.com"
    }
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["email"] == update_data["email"]

def test_delete_user(db_session):
    """사용자 삭제 테스트"""
    user_id = 1
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=5432)