# PostgreSQL 연결 TEST

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from dataclasses import dataclass
from typing import List, Dict, Optional
from pydantic import BaseModel

# 데이터베이스 설정
@dataclass
class DatabaseConfig:
    db_url: str = "postgresql://postgres:godlast@localhost:5432/postgres"

# Pydantic 모델
class TestItem(BaseModel):
    name: str
    value: int

class TestItemResponse(BaseModel):
    id: int
    name: str
    value: int
    created_at: Optional[str]

# FastAPI 앱 생성
app = FastAPI()

# 데이터베이스 연결 및 테이블 생성
def setup_database():
    engine = create_engine(DatabaseConfig().db_url)
    with engine.connect() as connection:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS public.test (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            value INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        connection.execute(text(create_table_query))
        connection.commit()
    return engine

# 전역 엔진 설정
engine = setup_database()

# API 엔드포인트
@app.post("/test/", response_model=TestItemResponse)
async def create_test_item(item: TestItem):
    with engine.connect() as connection:
        try:
            # 데이터 삽입
            insert_query = """
            INSERT INTO public.test (name, value)
            VALUES (:name, :value)
            RETURNING id, name, value, created_at
            """
            result = connection.execute(
                text(insert_query),
                {"name": item.name, "value": item.value}
            )
            connection.commit()
            row = result.fetchone()
            return {
                "id": row.id,
                "name": row.name,
                "value": row.value,
                "created_at": str(row.created_at)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/", response_model=List[TestItemResponse])
async def read_test_items():
    with engine.connect() as connection:
        try:
            select_query = "SELECT * FROM public.test ORDER BY id DESC"
            result = connection.execute(text(select_query))
            items = []
            for row in result:
                items.append({
                    "id": row.id,
                    "name": row.name,
                    "value": row.value,
                    "created_at": str(row.created_at)
                })
            return items
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# 테스트 코드
def test_create_and_read_items():
    client = TestClient(app)

    # 테스트 데이터 생성
    test_data = TestItem(name="테스트 아이템", value=100)

    # POST 요청 테스트
    response = client.post("/test/", json=test_data.model_dump())
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == test_data.name
    assert created_item["value"] == test_data.value

    # GET 요청 테스트
    response = client.get("/test/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) > 0
    assert items[0]["name"] == test_data.name
    assert items[0]["value"] == test_data.value

if __name__ == "__main__":
    # 테스트 실행
    test_create_and_read_items()
    print("모든 테스트가 성공적으로 완료되었습니다!")