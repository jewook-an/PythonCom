from common import HTTPClient

# base_url과 endpoint 분리
base_url = 'http://data.ex.co.kr/openapi'   # 한국도록공사 공공데이터 포털 API : TEST 용
client = HTTPClient(base_url)

# 기본 인증 설정
client.set_auth(('username', 'password'))

# 헤더 설정
client.set_headers({
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your-token'
})

# API 호출 및 결과 확인
try:
    # get() 메소드는 이미 JSON 데이터를 반환합니다
    response_data = client.get('/safeDriving/forecast', params={'key': 'test', 'type': 'json'})
    print("Response Data:", response_data)
except Exception as e:
    print("Error occurred:", str(e))

"""
# 하단부 TEST 시 주석해제(20241129)
# GET 요청
response_data = client.get('/users', params={'page': 1})

# POST 요청
response_data = client.post('/users', json_data={'name': 'John'})

# 파일 업로드
with open('file.pdf', 'rb') as f:
    response_data = client.upload_file('/upload', {'file': f})

# 파일 다운로드
client.download_file('/download/123', 'local_file.pdf')
"""