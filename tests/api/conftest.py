import pytest
import allure

from config.settings import settings
from config.settings import UserRole
from api.auth_api import AuthAPI
from api.leads_api import LeadsAPI
from utils.allure_helpers import attach_text, attach_env_info


@pytest.fixture(scope="session", autouse=True)
def session_setup():
    """Before/After session hook for all API tests.

    Before: Attaches environment info to Allure.
    After:  Logs session teardown.
    """
    attach_env_info(settings.ENV, settings.BASE_URL)
    attach_text(
        f"Admin: {settings.ADMIN_EMAIL}\n"
        f"API URL: {settings.API_BASE_URL}",
        name="Session Config",
    )
    yield
    # After session
    attach_text("API test session complete.", name="Session Teardown")


@pytest.fixture(scope="session")
def auth_api():
    """Provide an AuthAPI client instance."""
    return AuthAPI()


@pytest.fixture(scope="session")
def auth_token(auth_api: AuthAPI) -> str:
    """Authenticate as admin and return a valid JWT token for the session.

    Before: Logs authentication attempt.
    After: Token is cached for the session.
    """
    with allure.step("Before: Authenticate as Admin to obtain session token"):
        token = auth_api.login_and_get_token(settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)
        attach_text("Admin token obtained successfully.", name="Auth Setup")
    return token


@pytest.fixture(scope="function")
def leads_api(auth_token: str) -> LeadsAPI:
    """Provide an authenticated LeadsAPI client (Admin).

    Before: Client created with valid token.
    After:  Nothing to tear down (stateless HTTP client).
    """
    with allure.step("Before: Create authenticated LeadsAPI client"):
        client = LeadsAPI(token=auth_token)
    yield client


@pytest.fixture(scope="function")
def unauthenticated_leads_api() -> LeadsAPI:
    """Provide a LeadsAPI client without any authentication token."""
    with allure.step("Before: Create unauthenticated LeadsAPI client"):
        client = LeadsAPI()
    yield client


@pytest.fixture(scope="function")
def leads_api_for_role(request):
    """Parametrizable fixture: returns a LeadsAPI authenticated as the given UserRole.

    Usage:
        @pytest.mark.parametrize("leads_api_for_role", [UserRole.MANAGER], indirect=True)
    """
    role: UserRole = request.param
    with allure.step(f"Before: Authenticate as {role.value} and create LeadsAPI client"):
        auth = AuthAPI()
        user = settings.USERS[role]
        token = auth.login_and_get_token(user.email, user.password)
        attach_text(f"Authenticated as {role.value} ({user.email})", name="Role Auth")
        client = LeadsAPI(token=token)
    yield client
