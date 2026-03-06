import json
import allure


def attach_request(method: str, url: str, payload: dict = None, headers: dict = None):
    """Attach HTTP request details to the Allure report."""
    content = {
        "method": method,
        "url": url,
    }
    if headers:
        # Mask Authorization token for security
        safe_headers = {
            k: ("Bearer ***" if k.lower() == "authorization" else v)
            for k, v in headers.items()
        }
        content["headers"] = safe_headers
    if payload is not None:
        content["payload"] = payload

    allure.attach(
        json.dumps(content, indent=2, default=str),
        name="Request",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_response(response):
    """Attach HTTP response details to the Allure report."""
    try:
        body = response.json()
    except Exception:
        body = response.text

    content = {
        "status_code": response.status_code,
        "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 2),
        "body": body,
    }
    allure.attach(
        json.dumps(content, indent=2, default=str),
        name="Response",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_assertion(expected, actual, label: str = "Assertion"):
    """Attach expected vs actual comparison to the Allure report."""
    content = {
        "expected": expected,
        "actual": actual,
        "passed": expected == actual,
    }
    allure.attach(
        json.dumps(content, indent=2, default=str),
        name=label,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_screenshot(page, name: str = "Screenshot"):
    """Attach a Playwright page screenshot to the Allure report."""
    try:
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as e:
        allure.attach(
            f"Screenshot failed: {e}",
            name=f"{name} (ERROR)",
            attachment_type=allure.attachment_type.TEXT,
        )


def attach_page_url(page, label: str = "Current URL"):
    """Attach the current page URL to the Allure report."""
    allure.attach(
        page.url,
        name=label,
        attachment_type=allure.attachment_type.URI_LIST,
    )


def attach_text(content: str, name: str = "Info"):
    """Attach plain text to the Allure report."""
    allure.attach(
        str(content),
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


def attach_env_info(env: str, base_url: str):
    """Attach environment information to the Allure report."""
    content = {
        "environment": env,
        "base_url": base_url,
    }
    allure.attach(
        json.dumps(content, indent=2),
        name="Environment",
        attachment_type=allure.attachment_type.JSON,
    )
