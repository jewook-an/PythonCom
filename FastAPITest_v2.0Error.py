# 필요 패키지 : pip install fastapi motor pymongo pytest httpx
# MongoDB 연결 TEST

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
import asyncio
from datetime import datetime
import urllib.parse

# Pydantic 모델
class PyObjectId(ObjectId):
    @classmethod
    # def __get_validators__(cls):
    def _get_pydantic_core_schema_(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# 추가 : PyObjectId에 대한 pydantic-core schema 스키마 생성불가. 이 오류를 무시하려면 model_config에서 'arbitrary_types_allowed=True'를 설정해야 함
class TestItem(BaseModel):
    name: str
    value: int
    # Error 로 인한 추가
    class ConfigDict:
        arbitrary_types_allowed = True

class TestItemDB(TestItem):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # class Config:
    class ConfigDict:
        json_encoders = {ObjectId: str, datetime: str}
        arbitrary_types_allowed = True  # Error로 인한 추가
        # allow_population_by_field_name = True
        populate_by_name = True

# FastAPI 앱 생성
app = FastAPI()

# MongoDB 설정 : MongoDB 테이블 = 컬렉션
username = urllib.parse.quote_plus('TestUser')
password = urllib.parse.quote_plus('godlast')   # ! : 33 / @ : 64
chkParam = username + ":" + password
MONGODB_URL = "mongodb+srv://" + chkParam + "@cluster0.6ou1f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
"""
MONGODB_URL = "mongodb://localhost:27017"
"""
DB_NAME = "Cluster0"
COLLECTION_NAME = "test_items"

# MongoDB 연결
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# API 엔드포인트
@app.post("/test/", response_model=TestItemDB)
async def create_test_item(item: TestItem):
    try:
        # item_dict = item.dict()
        item_dict = item.model_dump()  # .dict() 대신 model_dump() 사용
        item_dict["created_at"] = datetime.utcnow()

        result = await app.mongodb[COLLECTION_NAME].insert_one(item_dict)

        created_item = await app.mongodb[COLLECTION_NAME].find_one(
            {"_id": result.inserted_id}
        )
        return TestItemDB(**created_item)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/", response_model=List[TestItemDB])
async def read_test_items():
    try:
        items = []
        cursor = app.mongodb[COLLECTION_NAME].find()
        async for document in cursor:
            items.append(TestItemDB(**document))
        return items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 테스트를 위한 비동기 컨텍스트 관리자
class AsyncTestClient:
    def __init__(self, app):
        self.app = app
        self.client = TestClient(app)

    async def __aenter__(self):
        # 테스트용 데이터베이스 연결
        self.app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
        self.app.mongodb = self.app.mongodb_client[DB_NAME + "_test"]
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 테스트 후 데이터베이스 정리
        await self.app.mongodb.drop_collection(COLLECTION_NAME)
        self.app.mongodb_client.close()

# 테스트 코드
async def test_create_and_read_items():
    async with AsyncTestClient(app) as client:
        # 테스트 데이터 생성
        test_data = {"name": "테스트 아이템", "value": 100}

        # POST 요청 테스트
        response = client.post("/test/", json=test_data)
        assert response.status_code == 200
        created_item = response.json()
        assert created_item["name"] == test_data["name"]
        assert created_item["value"] == test_data["value"]
        assert "_id" in created_item
        assert "created_at" in created_item

        # GET 요청 테스트
        response = client.get("/test/")
        assert response.status_code == 200
        items = response.json()
        assert len(items) > 0
        assert items[0]["name"] == test_data["name"]
        assert items[0]["value"] == test_data["value"]

# 메인 실행
if __name__ == "__main__":
    # 테스트 실행
    asyncio.run(test_create_and_read_items())
    print("모든 테스트가 성공적으로 완료되었습니다!")