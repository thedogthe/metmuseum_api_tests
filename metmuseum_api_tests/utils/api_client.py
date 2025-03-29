import logging
import requests
from typing import Optional, Dict, Any
from requests.exceptions import RequestException

class MetMuseumApiClient:
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"
    
    def __init__(self):
        self.session = requests.Session()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            self.logger.info(f"Making request to: {url} with params: {params}")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            self.logger.info(f"Response status: {response.status_code}")
            return response
        except RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
    
    def get_object(self, object_id: int):
        return self._make_request(f"objects/{object_id}")
    
    def search_objects(self, query: str, **kwargs):
        params = {"q": query, **kwargs}
        return self._make_request("search", params=params)
    
    def get_departments(self):
        return self._make_request("departments")