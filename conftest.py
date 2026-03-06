import os
import json
import pytest
import allure

from config.settings import settings


def pytest_configure(config):
    """Create required directories for reports and screenshots."""
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)


def pytest_sessionstart(session):
    """Write allure environment.properties so the report shows ENV context."""
    props = (
        f"Environment={settings.ENV}\n"
        f"Base.URL={settings.BASE_URL}\n"
        f"API.Base.URL={settings.API_BASE_URL}\n"
        f"Browser={settings.BROWSER}\n"
        f"Headless={settings.HEADLESS}\n"
    )
    env_file = os.path.join("reports", "allure-results", "environment.properties")
    os.makedirs(os.path.dirname(env_file), exist_ok=True)
    with open(env_file, "w") as f:
        f.write(props)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Global hook: runs after every test phase (setup / call / teardown).

    - Attaches test metadata to Allure for all tests.
    - For UI tests: takes a screenshot on failure and attaches it.
    - For API tests: the BaseAPI._log() handles per-call attachment automatically.
    """
    outcome = yield
    report = outcome.get_result()

    # Store the report on the item so fixtures can access it
    item._report = getattr(item, "_report", {})
    item._report[call.when] = report

    if call.when == "call" and report.failed:
        # ---- UI failure screenshot ----
        page = item.funcargs.get("page")
        if page is not None:
            try:
                screenshot_path = os.path.join(
                    "reports", "screenshots", f"{item.name}.png"
                )
                page.screenshot(path=screenshot_path, full_page=True)
                allure.attach(
                    page.screenshot(full_page=True),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(
                    page.url,
                    name="Failure URL",
                    attachment_type=allure.attachment_type.URI_LIST,
                )
            except Exception:
                pass

        # ---- Attach failure reason for all tests ----
        if report.longreprtext:
            allure.attach(
                report.longreprtext,
                name="Failure Details",
                attachment_type=allure.attachment_type.TEXT,
            )
