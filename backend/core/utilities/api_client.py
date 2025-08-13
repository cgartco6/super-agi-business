import requests
from typing import Dict, Any, Optional
from ..logging_setup import Logger
from ..error_handler import ErrorHandler

class APIClient:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.session = requests.Session()
        self.base_url = "http://localhost:8000"  # Would be configurable
        
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"GET request failed: {str(e)}")
            raise ErrorHandler.handle_error(e)

    def post(self, endpoint: str, data: Dict) -> Dict:
        """Make POST request"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"POST request failed: {str(e)}")
            raise ErrorHandler.handle_error(e)

    def put(self, endpoint: str, data: Dict) -> Dict:
        """Make PUT request"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"PUT request failed: {str(e)}")
            raise ErrorHandler.handle_error(e)

    def add_header(self, key: str, value: str):
        """Add header to session"""
        self.session.headers.update({key: value})
