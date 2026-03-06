from playwright.sync_api import Page, expect


class BasePage:
    """Base page object providing common methods for all pages.

    All page objects inherit from this class to reuse shared
    browser interaction patterns and assertions.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to the specified URL."""
        self.page.goto(url, wait_until="networkidle")

    def get_by_test_id(self, test_id: str):
        """Locate an element by its data-testid attribute."""
        return self.page.get_by_test_id(test_id)

    def fill_input(self, selector: str, value: str):
        """Clear and fill an input field."""
        element = self.page.locator(selector)
        element.clear()
        element.fill(value)

    def click(self, selector: str):
        """Click an element identified by the selector."""
        self.page.locator(selector).click()

    def get_text(self, selector: str) -> str:
        """Get the text content of an element."""
        return self.page.locator(selector).text_content() or ""

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if an element is visible on the page."""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_url(self, url_pattern: str, timeout: int = 15000):
        """Wait for the page URL to match a pattern."""
        self.page.wait_for_url(url_pattern, timeout=timeout)

    def wait_for_element(self, selector: str, state: str = "visible", timeout: int = 10000):
        """Wait for an element to reach the expected state."""
        self.page.locator(selector).wait_for(state=state, timeout=timeout)

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def take_screenshot(self, name: str = "screenshot"):
        """Capture a screenshot for debugging or reporting."""
        self.page.screenshot(path=f"reports/screenshots/{name}.png", full_page=True)
