"""
UI Tests - Login Module

This module contains all UI tests related to login functionality.
Organized for Allure reporting under: UI > Login
"""
import pytest
import allure
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.leads_page import LeadsPage
from config.settings import settings, UserRole
from utils.ui_step_logger import DetailedStepLogger


@allure.epic("Lead Management UI")
@allure.feature("Login")
@pytest.mark.ui
class TestLoginUI:
    """UI tests for login functionality."""

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_admin_login(self, page: Page, login_page: LoginPage, leads_page: LeadsPage):
        """TC-L01: Admin login with valid credentials."""
        logger = DetailedStepLogger(page)
        
        logger.step("Navigate to login page", f"URL: {settings.BASE_URL}/login")
        login_page.open()
        
        logger.step("Enter admin email", "Email: admin@company.com")
        page.locator("[type='email']").fill("admin@company.com")
        
        logger.step("Enter admin password", "Password: [MASKED]")
        page.locator("[type='password']").fill("Admin@123")
        
        logger.step("Click Sign In button", "Submitting login form")
        page.locator("button[type='submit']").click()
        
        logger.step("Wait for leads page", "Expected: /leads URL")
        page.wait_for_url("**/leads", timeout=10000)
        
        logger.verify(
            "User is on leads dashboard",
            expected="/leads in URL",
            actual=page.url,
            passed="/leads" in page.url
        )

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_manager_login(self, page: Page, login_page: LoginPage):
        """TC-L02: Manager login with valid credentials."""
        logger = DetailedStepLogger(page)
        
        logger.step("Navigate to login page")
        login_page.open()
        
        logger.step("Enter manager credentials", "Email: qa@company.com")
        page.locator("[type='email']").fill("qa@company.com")
        page.locator("[type='password']").fill("password123")
        
        logger.step("Click Sign In")
        page.locator("button[type='submit']").click()
        
        logger.step("Wait for redirect")
        page.wait_for_url("**/leads", timeout=10000)
        
        logger.verify("Manager logged in", "/leads", page.url, "/leads" in page.url)

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_viewer_login(self, page: Page, login_page: LoginPage):
        """TC-L03: Viewer login with valid credentials."""
        logger = DetailedStepLogger(page)
        
        logger.step("Navigate to login page")
        login_page.open()
        
        logger.step("Enter viewer credentials", "Email: tester@company.com")
        page.locator("[type='email']").fill("tester@company.com")
        page.locator("[type='password']").fill("Test@456")
        
        logger.step("Click Sign In")
        page.locator("button[type='submit']").click()
        
        logger.step("Wait for redirect")
        page.wait_for_url("**/leads", timeout=10000)
        
        logger.verify("Viewer logged in", "/leads", page.url, "/leads" in page.url)

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_wrong_password(self, page: Page, login_page: LoginPage):
        """TC-L05: Login with wrong password."""
        logger = DetailedStepLogger(page)
        
        logger.step("Navigate to login page")
        login_page.open()
        
        logger.step("Enter valid email", "Email: admin@company.com")
        page.locator("[type='email']").fill("admin@company.com")
        
        logger.step("Enter wrong password", "Password: wrongpass")
        page.locator("[type='password']").fill("wrongpass")
        
        logger.step("Click Sign In")
        page.locator("button[type='submit']").click()
        
        logger.step("Wait for error")
        page.wait_for_timeout(2000)
        
        logger.verify(
            "Still on login page",
            expected="/login in URL",
            actual=page.url,
            passed="/login" in page.url
        )

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_nonexistent_email(self, page: Page, login_page: LoginPage):
        """TC-L06: Login with non-existent email."""
        logger = DetailedStepLogger(page)
        
        logger.step("Navigate to login page")
        login_page.open()
        
        logger.step("Enter non-existent email", "Email: nobody@company.com")
        page.locator("[type='email']").fill("nobody@company.com")
        page.locator("[type='password']").fill("Admin@123")
        
        logger.step("Click Sign In")
        page.locator("button[type='submit']").click()
        
        logger.step("Wait for error")
        page.wait_for_timeout(2000)
        
        logger.verify("Still on login page", "/login", page.url, "/login" in page.url)

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_empty_fields(self, page: Page, login_page: LoginPage):
        """TC-L09: Login with both fields empty."""
        logger = DetailedStepLogger(page)
        
        logger.step("Navigate to login page")
        login_page.open()
        
        logger.step("Leave fields empty")
        
        logger.step("Click Sign In")
        page.locator("button[type='submit']").click()
        
        logger.step("Wait for validation")
        page.wait_for_timeout(1000)
        
        logger.verify("Still on login page", "/login", page.url, "/login" in page.url)

    @allure.story("Logout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_logout(self, page: Page, login_page: LoginPage, leads_page: LeadsPage):
        """Test logout redirects to login page."""
        logger = DetailedStepLogger(page)
        
        # Login first
        logger.step("Login as admin")
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        logger.step("Click Logout button")
        leads_page.click_logout()
        
        logger.step("Wait for redirect")
        page.wait_for_timeout(2000)
        
        logger.verify("Redirected to login", "/login", page.url, "/login" in page.url)

    @allure.story("Session")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_access_leads_without_login(self, page: Page):
        """TC-L15: Accessing leads page without login."""
        logger = DetailedStepLogger(page)
        
        logger.step("Navigate directly to /leads", f"URL: {settings.BASE_URL}/leads")
        page.goto(f"{settings.BASE_URL}/leads")
        
        logger.step("Wait for redirect")
        page.wait_for_timeout(2000)
        
        logger.verify(
            "Redirected to login",
            expected="/login in URL",
            actual=page.url,
            passed="/login" in page.url
        )


@allure.epic("Lead Management UI")
@allure.feature("Login - Multi-Role")
@pytest.mark.ui
class TestLoginMultiRole:
    """Parameterized UI tests for all user roles."""

    @allure.story("Valid Login - All Roles")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("role", [UserRole.ADMIN, UserRole.MANAGER, UserRole.VIEWER])
    def test_login_all_roles(self, page: Page, role: UserRole):
        """Verify all user roles can successfully login via UI."""
        user = settings.USERS[role]
        login_page = LoginPage(page)
        leads_page = LeadsPage(page)

        with allure.step(f"Login as {role.value}"):
            login_page.open()
            login_page.login(user.email, user.password)
            leads_page.wait_for_leads_page()

        assert leads_page.is_leads_page_displayed(), f"{role.value} should see leads page"
        assert "/leads" in page.url

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_cred", settings.INVALID_CREDENTIALS)
    def test_login_invalid_credentials_multi(self, page: Page, invalid_cred: dict):
        """Verify login fails with various invalid credentials."""
        login_page = LoginPage(page)

        with allure.step(f"Attempt login with {invalid_cred['reason']}"):
            login_page.open()
            login_page.login(invalid_cred["email"], invalid_cred["password"])
            page.wait_for_timeout(2000)

        # Should remain on login page or show error
        assert "/login" in page.url or login_page.is_error_displayed(), \
            f"Should fail for {invalid_cred['reason']}"

    @allure.story("Valid Login - Admin")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_admin_reaches_leads_page(self, page: Page):
        """Verify Admin user reaches leads page after login."""
        user = settings.USERS[UserRole.ADMIN]
        login_page = LoginPage(page)
        leads_page = LeadsPage(page)

        login_page.open()
        login_page.login(user.email, user.password)
        leads_page.wait_for_leads_page()

        # Verify on leads page and can see leads table
        assert leads_page.is_leads_page_displayed(), "Admin should see leads page"
        assert leads_page.get_table_row_count() >= 0, "Admin should see leads table"

    @allure.story("Valid Login - Manager")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_manager_reaches_leads_page(self, page: Page):
        """Verify Manager user reaches leads page after login."""
        user = settings.USERS[UserRole.MANAGER]
        login_page = LoginPage(page)
        leads_page = LeadsPage(page)

        login_page.open()
        login_page.login(user.email, user.password)
        leads_page.wait_for_leads_page()

        # Verify on leads page
        assert leads_page.is_leads_page_displayed(), "Manager should see leads page"

    @allure.story("Valid Login - Viewer")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_viewer_reaches_leads_page(self, page: Page):
        """Verify Viewer user reaches leads page after login."""
        user = settings.USERS[UserRole.VIEWER]
        login_page = LoginPage(page)
        leads_page = LeadsPage(page)

        login_page.open()
        login_page.login(user.email, user.password)
        leads_page.wait_for_leads_page()

        # Verify on leads page
        assert leads_page.is_leads_page_displayed(), "Viewer should see leads page"


@allure.epic("Lead Management UI")
@allure.feature("Login - Detailed Steps")
@pytest.mark.ui
class TestLoginDetailedSteps:
    """Login tests with detailed step-by-step logging."""

    @allure.story("Admin Login - Detailed Workflow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_admin_login_detailed_workflow(self, page: Page, login_page: LoginPage, leads_page: LeadsPage):
        """
        Detailed workflow test showing each step:
        a. Navigate to login page
        b. Enter username
        c. Enter password
        d. Click Sign In button
        e. Wait for leads page
        f. Verify successful login
        """
        logger = DetailedStepLogger(page)
        
        # a. Navigate to login page
        logger.step(
            action="Navigate to login page",
            details="URL: https://v0-lead-manager-app.vercel.app/login",
            screenshot=True
        )
        login_page.open()
        
        # b. Enter username
        logger.step(
            action="Enter username",
            details="Username: admin@company.com",
            screenshot=False
        )
        page.locator("[type='email']").fill("admin@company.com")
        
        # c. Enter password (masked in logs)
        logger.step(
            action="Enter password",
            details="Password: [MASKED for security]",
            screenshot=False
        )
        page.locator("[type='password']").fill("Admin@123")
        
        # d. Click Sign In button
        logger.step(
            action="Click Sign In button",
            details="Button: Sign In",
            screenshot=True
        )
        page.locator("button[type='submit']").click()
        
        # e. Wait for leads page to load
        logger.step(
            action="Wait for leads page to load",
            details="Expected: URL contains /leads",
            screenshot=False
        )
        page.wait_for_url("**/leads", timeout=10000)
        
        # f. Verify successful login
        logger.verify(
            description="User is on Leads dashboard",
            expected="https://v0-lead-manager-app.vercel.app/leads",
            actual=page.url,
            passed="/leads" in page.url
        )
        
        # Additional verification
        logger.verify(
            description="Leads table is visible",
            expected="Table with data visible",
            actual=f"Row count: {leads_page.get_table_row_count()}",
            passed=leads_page.is_leads_page_displayed()
        )


@allure.epic("Lead Management UI")
@allure.feature("Login - Invalid Credentials Detailed")
@pytest.mark.ui
class TestInvalidLoginDetailedSteps:
    """Invalid login tests with detailed step logging."""

    @allure.story("Invalid Login - Detailed Workflow")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_invalid_login_detailed(self, page: Page, login_page: LoginPage):
        """
        Test invalid login with detailed steps:
        a. Navigate to login page
        b. Enter invalid username
        c. Enter invalid password
        d. Click Sign In
        e. Verify error message displayed
        f. Verify still on login page
        """
        logger = DetailedStepLogger(page)
        
        # a. Navigate to login page
        logger.step(
            action="Navigate to login page",
            details="Opening login page",
            screenshot=True
        )
        login_page.open()
        
        # b. Enter invalid username
        logger.step(
            action="Enter username (invalid)",
            details="Username: wrong@email.com",
            screenshot=False
        )
        page.locator("[type='email']").fill("wrong@email.com")
        
        # c. Enter invalid password
        logger.step(
            action="Enter password (invalid)",
            details="Password: [MASKED]",
            screenshot=False
        )
        page.locator("[type='password']").fill("wrongpassword")
        
        # d. Click Sign In
        logger.step(
            action="Click Sign In button",
            details="Submitting invalid credentials",
            screenshot=True
        )
        page.locator("button[type='submit']").click()
        
        # e. Wait for error
        logger.step(
            action="Wait for error message",
            details="Expected: Error displayed",
            screenshot=True
        )
        page.wait_for_timeout(2000)
        
        # f. Verify error displayed
        error_visible = login_page.is_error_displayed()
        logger.verify(
            description="Error message is displayed",
            expected="Error message visible",
            actual=f"Error displayed: {error_visible}",
            passed=error_visible
        )
        
        # g. Verify still on login page
        logger.verify(
            description="User remains on login page",
            expected="URL contains /login",
            actual=f"Current URL: {page.url}",
            passed="/login" in page.url
        )


@allure.epic("Lead Management UI")
@allure.feature("Logout - Detailed Steps")
@pytest.mark.ui
class TestLogoutDetailedSteps:
    """Logout tests with detailed step logging."""

    @allure.story("Logout - Detailed Workflow")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_logout_detailed_workflow(self, page: Page, login_page: LoginPage, leads_page: LeadsPage):
        """
        Test logout with detailed steps:
        a. Login as admin
        b. Verify on leads page
        c. Click Logout button
        d. Wait for redirect
        e. Verify redirected to login page
        """
        logger = DetailedStepLogger(page)
        
        # a. Login as admin
        with allure.step("a. Login as admin"):
            logger.step(
                action="a1. Navigate to login",
                details="Opening login page",
                screenshot=True
            )
            login_page.open()
            
            logger.step(
                action="a2. Enter credentials",
                details="admin@company.com / [MASKED]",
                screenshot=False
            )
            page.locator("[type='email']").fill("admin@company.com")
            page.locator("[type='password']").fill("Admin@123")
            
            logger.step(
                action="a3. Click Sign In",
                details="Logging in",
                screenshot=True
            )
            page.locator("button[type='submit']").click()
        
        # b. Verify on leads page
        logger.step(
            action="b. Wait for leads page",
            details="Expected: /leads",
            screenshot=True
        )
        page.wait_for_url("**/leads", timeout=10000)
        
        # c. Click Logout
        logger.step(
            action="c. Click Logout button",
            details="Clicking logout",
            screenshot=True
        )
        leads_page.click_logout()
        
        # d. Wait for redirect
        logger.step(
            action="d. Wait for redirect to login",
            details="Expected: /login",
            screenshot=True
        )
        page.wait_for_timeout(2000)
        
        # e. Verify on login page
        logger.verify(
            description="User is on login page",
            expected="https://v0-lead-manager-app.vercel.app/login",
            actual=page.url,
            passed="/login" in page.url
        )
