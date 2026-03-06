import os
import pytest
import allure
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from config.settings import settings
from pages.login_page import LoginPage
from pages.leads_page import LeadsPage
from pages.create_lead_page import CreateLeadPage


@pytest.fixture(scope="session")
def browser():
    """Launch a browser instance for the entire test session."""
    with sync_playwright() as p:
        browser_type = getattr(p, settings.BROWSER)
        browser_instance = browser_type.launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO,
        )
        yield browser_instance
        browser_instance.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a fresh browser context per test with console error capture."""
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
        record_video_dir=None,
    )
    ctx.set_default_timeout(settings.TIMEOUT)

    # Capture browser console errors into Allure
    ctx.on("weberror", lambda err: allure.attach(
        str(err),
        name="Browser Error",
        attachment_type=allure.attachment_type.TEXT,
    ))

    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page and attach URL to Allure on teardown."""
    pg = context.new_page()

    # Log every navigation for traceability
    pg.on("framenavigated", lambda frame: allure.attach(
        frame.url,
        name=f"Navigated to",
        attachment_type=allure.attachment_type.URI_LIST,
    ) if frame == pg.main_frame else None)

    yield pg

    # After test: attach final URL and full-page screenshot regardless of outcome
    try:
        allure.attach(
            pg.url,
            name="Final URL",
            attachment_type=allure.attachment_type.URI_LIST,
        )
        allure.attach(
            pg.screenshot(full_page=True),
            name="Final State Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    pg.close()


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Provide a LoginPage instance."""
    return LoginPage(page)


@pytest.fixture(scope="function")
def leads_page(page: Page) -> LeadsPage:
    """Provide a LeadsPage instance."""
    return LeadsPage(page)


@pytest.fixture(scope="function")
def create_lead_page(page: Page) -> CreateLeadPage:
    """Provide a CreateLeadPage instance."""
    return CreateLeadPage(page)


@pytest.fixture(scope="function")
def logged_in_page(page: Page, login_page: LoginPage, leads_page: LeadsPage):
    """Provide a page that is already logged in as admin.

    Hooks:
    - Before: logs in as admin and attaches login step to Allure.
    - After:  handled by the page fixture (screenshot + URL).

    Returns:
        Tuple of (page, leads_page) after successful admin login.
    """
    with allure.step("Before: Login as Admin"):
        login_page.open()
        login_page.login_as_admin()
        leads_page.wait_for_leads_page()
        allure.attach(
            page.url,
            name="Post-Login URL",
            attachment_type=allure.attachment_type.URI_LIST,
        )
    return page, leads_page
