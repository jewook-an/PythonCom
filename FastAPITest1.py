import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from typing import List, Optional, Annotated
from datetime import datetime
import asyncio
from bson import ObjectId
import urllib

# ObjectId 변환을 위한 함수
def parse_objectid(value) -> ObjectId:
    if isinstance(value, str):
        return ObjectId(value)
    return value

# MongoDB ObjectId 타입 정의
PyObjectId = Annotated[ObjectId, BeforeValidator(parse_objectid)]

# Pydantic 모델
class TestItem(BaseModel):
    name: str
    value: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class TestItemDB(TestItem):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
    )

# MongoDB 설정
# MONGODB_URL = "mongodb://localhost:27017"
# DB_NAME = "testdb"
# COLLECTION_NAME = "test_items"

# MongoDB 설정 : MongoDB 테이블 = 컬렉션
username = urllib.parse.quote_plus('TestUser')
password = urllib.parse.quote_plus('godlast')   # ! : 33 / @ : 64
chkParam = username + ":" + password
MONGODB_URL = "mongodb+srv://" + chkParam + "@cluster0.6ou1f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Cluster0"
COLLECTION_NAME = "testuser"

# FastAPI 앱과 MongoDB 클라이언트 설정
app = FastAPI()
motor_client = AsyncIOMotorClient(MONGODB_URL)
app.mongodb_client = motor_client
app.mongodb = motor_client[DB_NAME]

# API 엔드포인트
@app.post("/testuser/", response_model=TestItemDB)
async def create_test_item(item: TestItem):
    try:
        item_dict = item.model_dump()
        item_dict["created_at"] = datetime.utcnow()

        result = await app.mongodb[COLLECTION_NAME].insert_one(item_dict)
        created_item = await app.mongodb[COLLECTION_NAME].find_one(
            {"_id": result.inserted_id}
        )
        return TestItemDB.model_validate(created_item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/testuser/", response_model=List[TestItemDB])
async def read_test_items():
    try:
        items = []
        cursor = app.mongodb[COLLECTION_NAME].find()
        async for document in cursor:
            items.append(TestItemDB.model_validate(document))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 테스트 함수
def run_tests():
    with TestClient(app) as client:

        print("\n=== 테스트 시작 ===")

        # 테스트 데이터베이스로 전환
        original_db = app.mongodb
        app.mongodb = app.mongodb_client[DB_NAME + "_test"]

    """
    Post 는 성공 > 응답은 받지 못함 (response.status_code=500)
    """
    try:
        # 1. POST 테스트
        print("\n1. POST 테스트 실행")
        test_data = {"name": "테스트 아이템", "value": 100}
        response = client.post("/testuser/", json=test_data)
        print(f"POST 응답 상태 코드: {response.status_code}")
        print(f"POST 응답 내용: {response.json()}")

        assert response.status_code == 200, f"예상 상태 코드: 200, 실제: {response.status_code}"
        created_item = response.json()
        assert created_item["name"] == test_data["name"], "이름이 일치하지 않습니다"
        assert created_item["value"] == test_data["value"], "값이 일치하지 않습니다"
        assert "_id" in created_item, "ID가 없습니다"
        print("POST 테스트 성공!")

        # 2. GET 테스트
        print("\n2. GET 테스트 실행")
        response = client.get("/testuser/")
        print(f"GET 응답 상태 코드: {response.status_code}")
        print(f"GET 응답 내용: {response.json()}")

        assert response.status_code == 200, f"예상 상태 코드: 200, 실제: {response.status_code}"
        items = response.json()
        assert len(items) > 0, "아이템이 없습니다"
        assert items[0]["name"] == test_data["name"], "이름이 일치하지 않습니다"
        assert items[0]["value"] == test_data["value"], "값이 일치하지 않습니다"
        print("GET 테스트 성공!")

        print("\n=== 모든 테스트 성공! ===")

    finally:
        # 테스트 데이터베이스 정리
        app.mongodb_client.drop_database(DB_NAME + "_test")
        # 원래 데이터베이스로 복구
        app.mongodb = original_db

if __name__ == "__main__":
    # MongoDB 연결 확인
    try:
        motor_client.server_info()
        print("MongoDB 연결 성공!")
        run_tests()
    except Exception as e:
        print(f"MongoDB 연결 실패: {str(e)}")
        exit(1)