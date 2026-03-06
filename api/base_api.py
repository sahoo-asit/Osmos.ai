import requests
from config.settings import settings
from utils.allure_helpers import attach_request, attach_response


class BaseAPI:
    """Base API client with common HTTP methods and authentication handling.

    Automatically attaches request and response details to Allure reports
    for every HTTP call, providing full visibility into API interactions.
    """

    def __init__(self, token: str = None):
        self.base_url = settings.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if token:
            self.set_auth_token(token)

    def set_auth_token(self, token: str):
        """Set the Authorization header with the Bearer token."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_auth_token(self):
        """Remove the Authorization header."""
        self.session.headers.pop("Authorization", None)

    def _log(self, method: str, url: str, payload: dict, response: requests.Response):
        """Attach request and response to Allure report."""
        try:
            attach_request(
                method=method,
                url=url,
                payload=payload,
                headers=dict(self.session.headers),
            )
            attach_response(response)
        except Exception:
            pass  # Never let reporting break the test

    def get(self, endpoint: str, params: dict = None, **kwargs) -> requests.Response:
        """Send a GET request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, **kwargs)
        self._log("GET", url, params, response)
        return response

    def post(self, endpoint: str, json: dict = None, **kwargs) -> requests.Response:
        """Send a POST request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=json, **kwargs)
        self._log("POST", url, json, response)
        return response

    def put(self, endpoint: str, json: dict = None, **kwargs) -> requests.Response:
        """Send a PUT request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=json, **kwargs)
        self._log("PUT", url, json, response)
        return response

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Send a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, **kwargs)
        self._log("DELETE", url, None, response)
        return response
