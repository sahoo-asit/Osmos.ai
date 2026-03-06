from api.base_api import BaseAPI


class AuthAPI(BaseAPI):
    """API client for authentication endpoints."""

    LOGIN_ENDPOINT = "/login"

    def login(self, email: str, password: str):
        """Authenticate a user and return the response.

        Args:
            email: User email address.
            password: User password.

        Returns:
            Response object from the login request.
        """
        payload = {"email": email, "password": password}
        response = self.post(self.LOGIN_ENDPOINT, json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("token"):
                self.set_auth_token(data["token"])
        return response

    def login_and_get_token(self, email: str, password: str) -> str:
        """Login and return just the token string.

        Args:
            email: User email address.
            password: User password.

        Returns:
            JWT token string.

        Raises:
            AssertionError: If login fails.
        """
        response = self.login(email, password)
        assert response.status_code == 200, f"Login failed with status {response.status_code}"
        data = response.json()
        assert data.get("success"), "Login response success is not True"
        return data["token"]
