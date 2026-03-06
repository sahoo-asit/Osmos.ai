"""
Detailed UI Step Logger for Allure Reporting.

This module provides granular step-by-step logging for UI automation,
making it easy to understand exactly what actions were performed.
"""
import allure
from playwright.sync_api import Page


def log_navigation(page: Page, url: str, description: str = "Loading URL"):
    """Log navigation to a URL with screenshot."""
    with allure.step(f"a. Navigate to: {url}"):
        page.goto(url)
        allure.attach(
            page.screenshot(full_page=True),
            name="Page Loaded",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            f"Loaded: {page.url}",
            name="URL",
            attachment_type=allure.attachment_type.URI_LIST
        )


def log_input(page: Page, field_name: str, value: str, locator: str = None):
    """Log entering text into a field."""
    with allure.step(f"b. Enter {field_name}: {value}"):
        if locator:
            field = page.locator(locator)
            field.fill(value)
        allure.attach(
            f"Field: {field_name}\nValue entered: {value}",
            name=f"Input: {field_name}",
            attachment_type=allure.attachment_type.TEXT
        )


def log_click(page: Page, button_name: str, locator: str = None):
    """Log clicking a button or element."""
    with allure.step(f"d. Click button: {button_name}"):
        if locator:
            page.locator(locator).click()
        allure.attach(
            f"Clicked: {button_name}",
            name=f"Action: Click",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            page.screenshot(full_page=True),
            name="After Click",
            attachment_type=allure.attachment_type.PNG
        )


def log_wait(page: Page, condition: str, timeout: int = 5000):
    """Log waiting for a condition."""
    with allure.step(f"c. Wait for: {condition}"):
        allure.attach(
            f"Waiting: {condition}\nTimeout: {timeout}ms",
            name="Wait Condition",
            attachment_type=allure.attachment_type.TEXT
        )


def log_verification(page: Page, expected: str, actual: str, check_name: str):
    """Log a verification/validation step with expected vs actual."""
    with allure.step(f"e. Verify: {check_name}"):
        allure.attach(
            f"Expected: {expected}\nActual: {actual}",
            name=f"Validation: {check_name}",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            page.screenshot(full_page=True),
            name="Verification State",
            attachment_type=allure.attachment_type.PNG
        )


def log_page_transition(page: Page, from_page: str, to_page: str):
    """Log page transitions."""
    with allure.step(f"f. Page transition: {from_page} -> {to_page}"):
        allure.attach(
            page.url,
            name="Current URL",
            attachment_type=allure.attachment_type.URI_LIST
        )
        allure.attach(
            page.screenshot(full_page=True),
            name=f"Now on: {to_page}",
            attachment_type=allure.attachment_type.PNG
        )


class DetailedStepLogger:
    """Helper class to log each UI action in a workflow format."""
    
    def __init__(self, page: Page):
        self.page = page
        self.step_number = 0
    
    def step(self, action: str, details: str = None, screenshot: bool = True):
        """Log a step with automatic numbering."""
        self.step_number += 1
        letter = chr(96 + self.step_number)  # a, b, c, d...
        
        with allure.step(f"{letter}. {action}"):
            if details:
                allure.attach(
                    details,
                    name="Details",
                    attachment_type=allure.attachment_type.TEXT
                )
            if screenshot:
                try:
                    allure.attach(
                        self.page.screenshot(full_page=True),
                        name="Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception:
                    pass
    
    def verify(self, description: str, expected, actual, passed: bool = None):
        """Log a verification step."""
        self.step_number += 1
        letter = chr(96 + self.step_number)
        
        with allure.step(f"{letter}. VERIFY: {description}"):
            allure.attach(
                f"Expected: {expected}\nActual: {actual}\nStatus: {'✓ PASS' if passed else '✗ FAIL' if passed is not None else 'N/A'}",
                name="Expected vs Actual",
                attachment_type=allure.attachment_type.TEXT
            )
            try:
                allure.attach(
                    self.page.screenshot(full_page=True),
                    name="Verification Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
