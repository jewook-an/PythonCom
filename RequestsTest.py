from common import RequestsCm

# 클라이언트 초기화
client = RequestsCm.HTTPClient('http://data.ex.co.kr/openapi/safeDriving/forecast?key=test&type=json')

# 기본 인증 설정
client.set_auth(('username', 'password'))

# 헤더 설정
client.set_headers({
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your-token'
})

# GET 요청
response = client.get('/users', params={'page': 1})

# POST 요청
response = client.post('/users', json_data={'name': 'John'})

# 파일 업로드
with open('file.pdf', 'rb') as f:
    response = client.upload_file('/upload', {'file': f})

# 파일 다운로드
client.download_file('/download/123', 'local_file.pdf')
