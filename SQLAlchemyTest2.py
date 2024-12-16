import urllib.parse
from mongoengine import connect, Document, StringField, EmailField, ValidationError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# 데이터베이스 매니저 초기화
# db_manager = DatabaseManager('postgresql://postgres:godlast@localhost/postgres')
# db_manager = DatabaseManager('postgresql://user:password@localhost/dbname')
#db_manager = DatabaseManager('mongodb://localhost:27017/dbname')

username = urllib.parse.quote_plus('TestUser')
password = urllib.parse.quote_plus('godlast')   # ! : 33 / @ : 64
chkParam = username + ":" + password

uri = "mongodb+srv://" + chkParam + "@cluster0.6ou1f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
print(uri)

# MongoDB에 연결
try:
    connect('cluster0', host=uri)
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    # connect('dbname', host='mongodb://username:password@cluster0.6ou1f.mongodb.net/?retryWrites=true&w=majority')
    print("MongoDB에 성공적으로 연결되었습니다.")
except Exception as e:
    print(f"MongoDB 연결 실패: {e}")

# 사용자 모델 정의
class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True)

# 테이블 생성 (MongoDB에서는 스키마가 없으므로 모델 정의로 대체)
# 데이터 추가
def create_user(username, email):
    try:
        user = User(username=username, email=email)
        user.save()
        print(f"사용자 {username}가 생성되었습니다.")
    except ValidationError as e:
        print(f"사용자 생성 실패: {e}")

# 사용자 조회
def read_user(username):
    try:
        user = User.objects.get(username=username)
        print(f"사용자 조회: {user.username}, 이메일: {user.email}")
    except User.DoesNotExist:
        print("사용자를 찾을 수 없습니다.")

# 사용자 업데이트
def update_user(username, new_username):
    try:
        user = User.objects.get(username=username)
        user.username = new_username
        user.save()
        print(f"사용자 {username}가 {new_username}로 업데이트되었습니다.")
    except User.DoesNotExist:
        print("사용자를 찾을 수 없습니다.")
    except ValidationError as e:
        print(f"사용자 업데이트 실패: {e}")

# 사용자 삭제
def delete_user(username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"사용자 {username}가 삭제되었습니다.")
    except User.DoesNotExist:
        print("사용자를 찾을 수 없습니다.")

# 사용 예시
# create_user("testuser1", "user1@example.com")
read_user("testuser1")
# update_user("testuser1", "newusername")
# delete_user("newusername")

"""
db_manager = DatabaseManager(uri)

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

"""