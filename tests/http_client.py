import requests
from typing import Optional, Dict, Any


class HttpClient:
    
    def __init__(self, base_url: str, timeout: int = 10):

        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:

        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        return response
    
    def get_json(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:

        response = self.get(endpoint, params)
        response.raise_for_status()
        return response.json()
    
    def close(self):
        self.session.close()
