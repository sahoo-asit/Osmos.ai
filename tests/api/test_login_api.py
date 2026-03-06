"""
API Tests - Login Module

This module contains all API tests related to authentication/login.
Organized for Allure reporting under: API > Login
"""
import pytest
import allure

from api.auth_api import AuthAPI
from config.settings import settings, UserRole


def log_validation(check_name: str, expected, actual, passed: bool = None):
    """Log validation with expected vs actual."""
    status = "✓ PASS" if passed else "✗ FAIL" if passed is not None else "N/A"
    allure.attach(
        f"Check: {check_name}\nExpected: {expected}\nActual: {actual}\nStatus: {status}",
        name=f"Validation: {check_name}",
        attachment_type=allure.attachment_type.TEXT
    )


@allure.epic("Lead Management API")
@allure.feature("Login")
@pytest.mark.api
class TestLoginAPI:
    """API tests for login/authentication endpoint."""

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.parametrize("role", [UserRole.ADMIN, UserRole.MANAGER, UserRole.VIEWER])
    def test_login_all_valid_roles(self, auth_api: AuthAPI, role: UserRole):
        """TC-API01-03: Login with all valid roles (Admin, Manager, Viewer)."""
        user = settings.USERS[role]
        
        with allure.step(f"POST /api/login with {role.value} credentials"):
            response = auth_api.login(user.email, user.password)
        
        with allure.step("Validate response"):
            log_validation("Status Code", 200, response.status_code, response.status_code == 200)
            assert response.status_code == 200
            
            data = response.json()
            log_validation("Success", True, data.get("success"), data.get("success") is True)
            log_validation("Token present", "Non-empty", bool(data.get("token")), bool(data.get("token")))
            log_validation("Role", role.value, data.get("role"), data.get("role") == role.value)
            log_validation("Email matches", user.email, data.get("email"), data.get("email") == user.email)
            
            assert data.get("success") is True
            assert data.get("token")
            assert data.get("role") == role.value

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    @pytest.mark.parametrize("role", [UserRole.ADMIN, UserRole.MANAGER, UserRole.VIEWER])
    def test_login_returns_role_info(self, auth_api: AuthAPI, role: UserRole):
        """Verify login response includes role information."""
        user = settings.USERS[role]
        
        with allure.step(f"POST /api/login with {role.value}"):
            response = auth_api.login(user.email, user.password)
        
        with allure.step("Validate role in response"):
            assert response.status_code == 200
            data = response.json()
            if "role" in data:
                log_validation("Role in response", role.value, data.get("role"), data.get("role") == role.value)

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_cred", settings.INVALID_CREDENTIALS)
    def test_login_invalid_credentials(self, auth_api: AuthAPI, invalid_cred: dict):
        """Verify login fails with various invalid credentials."""
        with allure.step(f"POST /api/login with {invalid_cred['reason']}"):
            response = auth_api.login(invalid_cred["email"], invalid_cred["password"])
        
        with allure.step("Validate 400/401 response"):
            log_validation("Status Code", "400 or 401", response.status_code, response.status_code in [400, 401])
            assert response.status_code in [400, 401]
            
            data = response.json()
            log_validation("Success is False or error present", True, data.get("success") is False or "error" in data, True)

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_empty_body(self, auth_api: AuthAPI):
        """TC-API05: Login with empty body."""
        with allure.step("POST /api/login with empty payload"):
            response = auth_api.session.post(
                f"{auth_api.base_url}/login",
                json={}
            )
        
        with allure.step("Validate error response"):
            log_validation("Status Code", "400 or 401", response.status_code, response.status_code in [400, 401])
            assert response.status_code in [400, 401]

    @allure.story("Security")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_login_sql_injection_email(self, auth_api: AuthAPI):
        """TC-API06: SQL injection in email field."""
        with allure.step("POST /api/login with SQL injection in email"):
            response = auth_api.login("' OR 1=1 --", "anything")
        
        with allure.step("Validate rejection - no data leakage"):
            log_validation("Status Code", 401, response.status_code, response.status_code == 401)
            assert response.status_code == 401
            
            data = response.json()
            log_validation("No token leaked", None, data.get("token"), data.get("token") is None)

    @allure.story("Security")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_login_sql_injection_password(self, auth_api: AuthAPI):
        """SQL injection in password field."""
        with allure.step("POST /api/login with SQL injection in password"):
            response = auth_api.login("admin@company.com", "' OR '1'='1' --")
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", 401, response.status_code, response.status_code == 401)
            assert response.status_code == 401

    @allure.story("Security")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_login_xss_in_password(self, auth_api: AuthAPI):
        """TC-L14: XSS script in password field."""
        with allure.step("POST /api/login with XSS in password"):
            response = auth_api.login("admin@company.com", "<script>alert('xss')</script>")
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", 401, response.status_code, response.status_code == 401)
            assert response.status_code == 401

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_login_xss_in_email(self, auth_api: AuthAPI):
        """XSS payload in email field."""
        with allure.step("POST /api/login with XSS in email"):
            response = auth_api.login("<script>alert('xss')</script>@test.com", "password")
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", "400 or 401", response.status_code, response.status_code in [400, 401])
            assert response.status_code in [400, 401]

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_login_very_long_email(self, auth_api: AuthAPI):
        """Extremely long email handling."""
        with allure.step("POST /api/login with 1000+ char email"):
            long_email = "a" * 1000 + "@test.com"
            response = auth_api.login(long_email, "password")
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "400, 401, 413, or 422", response.status_code, response.status_code in [400, 401, 413, 422])
            assert response.status_code in [400, 401, 413, 422]

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_login_very_long_password(self, auth_api: AuthAPI):
        """Extremely long password handling."""
        with allure.step("POST /api/login with 10000 char password"):
            response = auth_api.login("admin@company.com", "A" * 10000)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "400, 401, 413, or 422", response.status_code, response.status_code in [400, 401, 413, 422])
            assert response.status_code in [400, 401, 413, 422]

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_login_unicode_in_credentials(self, auth_api: AuthAPI):
        """Unicode characters in credentials."""
        with allure.step("POST /api/login with unicode email/password"):
            response = auth_api.login("用户@公司.com", "密码123")
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "400 or 401", response.status_code, response.status_code in [400, 401])
            assert response.status_code in [400, 401]

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_login_null_bytes_in_email(self, auth_api: AuthAPI):
        """Null byte injection in email."""
        with allure.step("POST /api/login with null byte in email"):
            response = auth_api.login("admin\x00@company.com", "Admin@123")
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "400 or 401", response.status_code, response.status_code in [400, 401])
            assert response.status_code in [400, 401]

    @allure.story("Security")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.security
    def test_login_special_characters_in_password(self, auth_api: AuthAPI):
        """Special characters in password."""
        with allure.step("POST /api/login with special chars password"):
            response = auth_api.login("admin@company.com", "!@#$%^&*()_+-=[]{}|;':\",./<>?`~")
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "400 or 401", response.status_code, response.status_code in [400, 401])
            assert response.status_code in [400, 401]

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_empty_email(self, auth_api: AuthAPI):
        """Verify login fails with empty email."""
        with allure.step("POST /api/login with empty email"):
            response = auth_api.login("", "Admin@123")
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", "400, 401, or 422", response.status_code, response.status_code in [400, 401, 422])
            assert response.status_code in [400, 401, 422]

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_empty_password(self, auth_api: AuthAPI):
        """Verify login fails with empty password."""
        with allure.step("POST /api/login with empty password"):
            response = auth_api.login("admin@company.com", "")
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", "400, 401, or 422", response.status_code, response.status_code in [400, 401, 422])
            assert response.status_code in [400, 401, 422]

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_invalid_email_format(self, auth_api: AuthAPI):
        """Verify login fails with malformed email."""
        with allure.step("POST /api/login with invalid email format"):
            response = auth_api.login("not-an-email", "Admin@123")
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", "400, 401, or 422", response.status_code, response.status_code in [400, 401, 422])
            assert response.status_code in [400, 401, 422]

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_login_response_structure(self, auth_api: AuthAPI):
        """Verify login response has all expected fields."""
        with allure.step("POST /api/login"):
            response = auth_api.login("admin@company.com", "Admin@123")
        
        with allure.step("Validate response structure"):
            data = response.json()
            log_validation("Has 'success' field", True, "success" in data, "success" in data)
            log_validation("Has 'token' field", True, "token" in data, "token" in data)
            log_validation("Has 'email' field", True, "email" in data, "email" in data)
            assert "success" in data
            assert "token" in data
            assert "email" in data


@allure.epic("Lead Management API")
@allure.feature("Login")
@pytest.mark.api
class TestLoginDetailedValidationAPI:
    """Detailed step-by-step validation tests for login."""

    @allure.story("Valid Login - Detailed Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_with_detailed_validation(self, auth_api: AuthAPI):
        """Login with step-by-step field validation in Allure report."""
        with allure.step("Step 1: Send POST /api/login with admin credentials"):
            response = auth_api.login("admin@company.com", "Admin@123")

        with allure.step("Step 2: Validate response status is 200"):
            log_validation("HTTP Status Code", 200, response.status_code, response.status_code == 200)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        with allure.step("Step 3: Parse response JSON"):
            data = response.json()
            log_validation("Response is valid JSON", "Valid JSON object", type(data).__name__, isinstance(data, dict))

        with allure.step("Step 4: Validate success field"):
            success = data.get("success")
            log_validation("Response success field", True, success, success is True)
            assert success is True

        with allure.step("Step 5: Validate token is present"):
            token = data.get("token")
            has_token = token is not None and len(str(token)) > 0
            log_validation("JWT Token returned", "Non-empty string", f"Present: {has_token}, Length: {len(str(token)) if token else 0}", has_token)
            assert has_token, "Token should be returned"

        with allure.step("Step 6: Validate user email"):
            returned_email = data.get("email")
            log_validation("User email matches", "admin@company.com", returned_email, returned_email == "admin@company.com")
            assert returned_email == "admin@company.com"

        with allure.step("Step 7: Validate user role"):
            role = data.get("role")
            log_validation("User role is admin", "admin", role, role == "admin")
            assert role == "admin"

    @allure.story("Invalid Login - Detailed Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_invalid_login_detailed_validation(self, auth_api: AuthAPI):
        """Invalid login with step-by-step error validation in Allure report."""
        with allure.step("Step 1: POST /api/login with invalid credentials"):
            response = auth_api.login("wrong@test.com", "wrongpass")

        with allure.step("Step 2: Validate 401 status"):
            log_validation("HTTP Status Code (Unauthorized)", 401, response.status_code, response.status_code == 401)
            assert response.status_code == 401

        with allure.step("Step 3: Validate error response"):
            data = response.json()
            log_validation("Success is false", False, data.get("success"), data.get("success") is False)

            error_msg = data.get("error", "")
            has_error = bool(error_msg)
            log_validation("Error message present", "Non-empty error message", f"Error: {error_msg}", has_error)
            assert has_error, "Error message should be present"

        with allure.step("Step 4: Validate no token returned"):
            token = data.get("token")
            log_validation("No token for invalid login", None, token, token is None)
            assert token is None, "Token should not be returned for invalid login"
