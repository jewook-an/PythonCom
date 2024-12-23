from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List
import urllib

# MongoDB Atlas 연결
username = urllib.parse.quote_plus('TestUser')
password = urllib.parse.quote_plus('godlast')   # ! : 33 / @ : 64
# MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.6ou1f.mongodb.net/cluster0?retryWrites=true&w=majority"
DB_NAME = "Cluster0"
COLLECTION_NAME = "testuser"

client = MongoClient(MONGO_URI)
db = client["test_db"]  # 사용할 데이터베이스 이름
collection = db["test_collection"]  # 사용할 컬렉션 이름

# FastAPI 앱 생성
app = FastAPI()

# 데이터 모델 정의
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    in_stock: bool

class ItemResponse(Item):
    id: str

# ObjectId 변환 헬퍼 함수
def object_id_to_str(obj_id):
    return str(obj_id)

# CRUD 엔드포인트 구현
@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    item_dict = item.dict()
    result = collection.insert_one(item_dict)
    item_dict["id"] = object_id_to_str(result.inserted_id)
    return item_dict

@app.get("/items/", response_model=List[ItemResponse])
async def get_items():
    items = list(collection.find())
    for item in items:
        item["id"] = object_id_to_str(item["_id"])
        del item["_id"]
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item["id"] = object_id_to_str(item["_id"])
    del item["_id"]
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: Item):
    result = collection.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict()},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    result["id"] = object_id_to_str(result["_id"])
    del result["_id"]
    return result

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

import httpx
# 테스트 데이터 생성
test_item = {
    "name": "Sample Item",
    "description": "This is a test item.",
    "price": 9.99,
    "in_stock": True
}

# create_item 테스트 함수
def test_create_item():
    response = httpx.post(f"{MONGO_URI}/items/", json=test_item)
    if response.status_code == 200:
        print("Test Passed!")
        print("Response:", response.json())
    else:
        print("Test Failed!")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    # MongoDB 연결 확인
    try:
        test_create_item()
    except Exception as e:
        print(f"MongoDB 연결 실패: {str(e)}")
        exit(1)