import requests
import json
from typing import Dict, Any, Optional
from urllib.parse import urljoin
import logging

class HTTPClient:
    """
    HTTP 요청을 처리하기 위한 재사용 가능한 클래스
    """

    def __init__(self, base_url: str, timeout: int = 30):
        """
        HTTPClient 초기화

        Args:
            base_url (str): API의 기본 URL
            timeout (int): 요청 타임아웃 (초)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def _build_url(self, endpoint: str) -> str:
        """
        전체 URL 생성
        """
        return urljoin(f"{self.base_url}/", endpoint.lstrip('/'))

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        응답 처리 및 에러 체크
        """
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.JSONDecodeError:
            self.logger.error(f"JSON 디코딩 실패: {response.text}")
            raise
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP 에러: {str(e)}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        GET 요청 수행
        """
        url = self._build_url(endpoint)
        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        POST 요청 수행
        """
        url = self._build_url(endpoint)
        response = self.session.post(
            url,
            data=data,
            json=json_data,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        PUT 요청 수행
        """
        url = self._build_url(endpoint)
        response = self.session.put(
            url,
            data=data,
            json=json_data,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        DELETE 요청 수행
        """
        url = self._build_url(endpoint)
        response = self.session.delete(
            url,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def upload_file(self, endpoint: str, files: Dict, **kwargs) -> Dict[str, Any]:
        """
        파일 업로드
        """
        url = self._build_url(endpoint)
        response = self.session.post(
            url,
            files=files,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def download_file(self, endpoint: str, local_filename: str, **kwargs) -> str:
        """
        파일 다운로드
        """
        url = self._build_url(endpoint)
        response = self.session.get(
            url,
            stream=True,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()

        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return local_filename

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        세션 헤더 설정
        """
        self.session.headers.update(headers)

    def set_auth(self, auth: tuple) -> None:
        """
        기본 인증 설정
        """
        self.session.auth = auth

    def set_timeout(self, timeout: int) -> None:
        """
        타임아웃 설정
        """
        self.timeout = timeout
