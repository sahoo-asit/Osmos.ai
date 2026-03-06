from pages.base_page import BasePage
from config.settings import settings


class LoginPage(BasePage):
    """Page object for the Login page of Lead Manager application."""

    # Locators
    FORM_CONTAINER = "[data-testid='login-form-container']"
    LOGIN_FORM = "[data-testid='login-form']"
    EMAIL_INPUT = "[data-testid='login-form'] input[type='email'], [data-testid='login-form'] input[name='email'], [data-testid='login-form-container'] input[placeholder*='company.com']"
    PASSWORD_INPUT = "[data-testid='login-form'] input[type='password'], [data-testid='login-form'] input[name='password'], [data-testid='login-form-container'] input[placeholder*='password']"
    SIGN_IN_BUTTON = "[data-testid='login-form'] button[type='submit'], [data-testid='login-form-container'] button:has-text('Sign in')"
    ERROR_MESSAGE = "[data-testid='login-error-alert'], [role='alert']:has-text('Invalid'), .text-destructive:has-text('Invalid')"

    def open(self):
        """Navigate to the login page."""
        self.navigate(settings.LOGIN_URL)
        self.page.wait_for_selector(self.FORM_CONTAINER, state="visible", timeout=15000)
        return self

    def enter_email(self, email: str):
        """Enter email address in the email field."""
        self.page.locator(self.EMAIL_INPUT).first.clear()
        self.page.locator(self.EMAIL_INPUT).first.fill(email)
        return self

    def enter_password(self, password: str):
        """Enter password in the password field."""
        self.page.locator(self.PASSWORD_INPUT).first.clear()
        self.page.locator(self.PASSWORD_INPUT).first.fill(password)
        return self

    def click_sign_in(self):
        """Click the Sign In button."""
        self.page.locator(self.SIGN_IN_BUTTON).first.click()
        return self

    def login(self, email: str, password: str):
        """Perform complete login flow.

        Args:
            email: User email address.
            password: User password.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_sign_in()
        return self

    def login_as_admin(self):
        """Login with admin credentials from settings."""
        return self.login(settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)

    def is_login_page_displayed(self) -> bool:
        """Check if the login form is visible."""
        return self.is_visible(self.FORM_CONTAINER)

    def get_error_message(self) -> str:
        """Get the error message displayed on failed login."""
        self.page.wait_for_selector(self.ERROR_MESSAGE, state="visible", timeout=5000)
        return self.page.locator(self.ERROR_MESSAGE).first.text_content() or ""

    def is_error_displayed(self) -> bool:
        """Check if an error message is shown."""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)
