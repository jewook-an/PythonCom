from common import DatabaseManager, User


# 데이터베이스 매니저 초기화
db_manager = DatabaseManager('postgresql://postgres:godlast@localhost/postgres')
# db_manager = DatabaseManager('postgresql://user:password@localhost/dbname')
#db_manager = DatabaseManager('mongodb://localhost:27017/dbname')

# 테이블 생성
db_manager.create_tables()

# 새 사용자 추가
new_user = User(email="user1@example.com", username="testuser1")
user = db_manager.add_item(new_user)

# ID로 사용자 조회
user = db_manager.get_by_id(User, 1)
print(user)

# 필터로 사용자 조회
users = db_manager.get_by_filter(User, {"username": "testuser1"})
print(users)

# 사용자 정보 업데이트
updated_user = db_manager.update_item(User, 1, {"username": "newusername"})
print(updated_user)

# 사용자 삭제
# db_manager.delete_item(User, 1)

# Raw SQL 실행
results = db_manager.execute_raw_query(
    "SELECT * FROM users WHERE email LIKE :email",
    {"email": "%@example.com"}
)
print(f"Raw SQL 실행 : 결과: {results}")