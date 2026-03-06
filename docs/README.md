# Lead Manager — QA Automation Framework

A production-grade **Python + Pytest** test automation framework for the Lead Manager SaaS application, covering **manual test cases**, **UI automation** (Playwright), and **API testing** (Requests).

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Test Credentials](#test-credentials)
5. [Running Tests](#running-tests)
6. [Writing New Tests](#writing-new-tests)
7. [Framework Architecture](#framework-architecture)
8. [Configuration](#configuration)
9. [Debugging Guide](#debugging-guide)
10. [CI/CD Integration](#cicd-integration)
11. [FAQ](#faq)

---

## Overview

### What This Framework Covers

| Part | Description | Location |
|------|-------------|----------|
| **Part 1: Manual Test Cases** | 35+ documented test cases for Login → Create Lead → List Lead | `docs/manual_test_cases.md` |
| **Part 2: UI Automation** | Playwright-based E2E tests with Page Object Model | `tests/ui/` |
| **Part 3: API Testing** | Comprehensive API tests with role-based access | `tests/api/` |

### Application Under Test

- **UI URL**: https://v0-lead-manager-app.vercel.app
- **API Base URL**: https://v0-lead-manager-app.vercel.app/api

---

## Project Structure

```
Osmos.ai/
├── config/
│   └── settings.py             # Centralized config, user roles, credentials
├── pages/                      # Page Object Model (UI)
│   ├── base_page.py            # Common page interactions
│   ├── login_page.py           # Login page object
│   ├── leads_page.py           # Leads listing page object
│   └── create_lead_page.py     # Create lead dialog (all fields)
├── api/                        # API Client Layer
│   ├── base_api.py             # Base HTTP client with auth
│   ├── auth_api.py             # Authentication API client
│   └── leads_api.py            # Leads CRUD API client
├── tests/
│   ├── ui/                     # UI automation tests
│   │   ├── conftest.py         # Browser & page fixtures
│   │   ├── test_lead_management_flow.py  # E2E flow tests
│   │   └── test_login_roles.py # Multi-role login tests
│   └── api/                    # API tests
│       ├── conftest.py         # API client fixtures
│       ├── test_auth_api.py    # Auth API tests
│       ├── test_auth_api_roles.py  # Multi-role auth tests
│       ├── test_leads_api.py   # Basic leads API tests
│       └── test_leads_api_comprehensive.py  # Full coverage
├── utils/
│   └── helpers.py              # Test data generators (Faker)
├── docs/
│   └── manual_test_cases.md    # Part 1: Manual test cases
├── reports/                    # Generated after test run
│   ├── report.html             # Pytest HTML report
│   ├── screenshots/            # Failure screenshots
│   └── allure-results/         # Allure report data
├── .env                        # Environment configuration
├── pytest.ini                  # Pytest configuration & markers
├── requirements.txt            # Python dependencies
├── run.sh                      # One-click test runner
└── README.md                   # This file
```

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- macOS, Linux, or Windows with WSL

### One-Command Setup & Run

```bash
# Clone the repository
git clone <repo-url>
cd Osmos.ai

# Make run script executable and run
chmod +x run.sh
./run.sh
```

The script automatically:
1. Creates a Python virtual environment (`.venv/`)
2. Installs all dependencies from `requirements.txt`
3. Installs Playwright browsers (Chromium)
4. Runs all tests (API + UI)
5. Generates HTML + Allure reports in `reports/`

### Manual Setup (Alternative)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium

# Run tests
pytest
```

---

## Test Credentials

The application has 3 user roles with different permissions:

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| **Admin** | `admin@company.com` | `Admin@123` | Create, Edit, Delete, View, Export |
| **Manager** | `qa@company.com` | `password123` | Create, Edit, View, Export (No Delete) |
| **Viewer** | `tester@company.com` | `Test@456` | View only (Read-only) |

### Invalid Credentials for Negative Testing

| Scenario | Email | Password |
|----------|-------|----------|
| Wrong Password | `admin@company.com` | `wrongpass` |
| Unregistered Email | `unknown@test.com` | `password123` |
| Invalid Email Format | `notanemail` | `password123` |
| Empty Fields | (empty) | (empty) |

---

## Running Tests

### Using run.sh (Recommended)

```bash
./run.sh                    # Run all tests
./run.sh --api              # Run API tests only
./run.sh --ui               # Run UI tests only
./run.sh --smoke            # Run smoke tests only
./run.sh --ui --headed      # Run UI tests with visible browser
./run.sh --report           # Run all & open HTML report
```

### Using Pytest Directly

```bash
source .venv/bin/activate

# Run all tests
pytest

# Run by marker
pytest -m api               # API tests only
pytest -m ui                # UI tests only
pytest -m smoke             # Critical path tests
pytest -m positive          # Positive scenarios
pytest -m negative          # Negative scenarios
pytest -m boundary          # Boundary tests

# Run specific test file
pytest tests/api/test_auth_api.py -v
pytest tests/ui/test_lead_management_flow.py -v

# Run specific test
pytest tests/api/test_auth_api.py::TestAuthAPI::test_login_valid_admin -v

# Run with extra verbosity
pytest -v --tb=long

# Run in parallel (faster)
pytest -n auto
```

### Viewing Reports

```bash
# HTML Report (opens in browser)
open reports/report.html

# Allure Report (interactive)
allure serve reports/allure-results
```

---

## Writing New Tests

### Adding a New API Test

1. Create test file in `tests/api/` (e.g., `test_new_feature.py`)
2. Use existing fixtures from `conftest.py`

```python
import pytest
import allure
from api.leads_api import LeadsAPI
from utils.helpers import generate_api_lead_payload

@allure.epic("Lead Management")
@allure.feature("New Feature")
@pytest.mark.api
class TestNewFeature:
    
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_new_functionality(self, leads_api: LeadsAPI):
        """Test description here."""
        payload = generate_api_lead_payload()
        response = leads_api.create_lead(payload)
        assert response.status_code == 201
```

### Adding a New UI Test

1. Create test file in `tests/ui/` (e.g., `test_new_flow.py`)
2. Use page objects from `pages/`

```python
import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.leads_page import LeadsPage

@allure.epic("Lead Management")
@allure.feature("New Flow")
@pytest.mark.ui
class TestNewFlow:
    
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_new_user_flow(self, page: Page):
        """Test description here."""
        login_page = LoginPage(page)
        leads_page = LeadsPage(page)
        
        login_page.open()
        login_page.login_as_admin()
        leads_page.wait_for_leads_page()
        
        assert leads_page.is_leads_page_displayed()
```

### Adding a New Page Object

1. Create file in `pages/` (e.g., `edit_lead_page.py`)
2. Inherit from `BasePage`

```python
from pages.base_page import BasePage

class EditLeadPage(BasePage):
    """Page object for Edit Lead dialog."""
    
    # Locators
    DIALOG = "[role='dialog']"
    SAVE_BUTTON = "button:has-text('Save')"
    
    def save_changes(self):
        self.page.locator(self.SAVE_BUTTON).click()
        return self
```

### Test Markers

Use these markers to categorize tests:

```python
@pytest.mark.ui          # UI automation test
@pytest.mark.api         # API test
@pytest.mark.smoke       # Critical path test
@pytest.mark.regression  # Full regression test
@pytest.mark.positive    # Positive scenario
@pytest.mark.negative    # Negative scenario
@pytest.mark.boundary    # Boundary/edge case
```

---

## Framework Architecture

### Design Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|--------|
| **Page Object Model** | `pages/*.py` | UI logic encapsulation, maintainability |
| **API Client Pattern** | `api/*.py` | Reusable HTTP clients with auth |
| **Fixture Injection** | `conftest.py` | Dependency injection, setup/teardown |
| **Data Factory** | `utils/helpers.py` | Realistic test data generation |
| **Configuration** | `config/settings.py` | Centralized, environment-based config |

### Key Components

#### Page Objects (`pages/`)

- **BasePage**: Common methods (navigate, click, fill, wait)
- **LoginPage**: Login form interactions
- **LeadsPage**: Leads table, search, filters, pagination
- **CreateLeadPage**: All form fields (name, email, phone, company, etc.)

#### API Clients (`api/`)

- **BaseAPI**: HTTP methods (GET, POST, PUT, DELETE), auth token handling
- **AuthAPI**: Login endpoint, token management
- **LeadsAPI**: CRUD operations for leads

#### Test Data (`utils/helpers.py`)

- `generate_lead_data()` - Full lead with all fields
- `generate_api_lead_payload()` - API-compatible payload
- `generate_minimal_lead_payload()` - Required fields only
- `generate_boundary_test_data()` - Edge case data
- `generate_security_test_payloads()` - Security test data

---

## Configuration

### Environment Variables (`.env`)

```env
BASE_URL=https://v0-lead-manager-app.vercel.app
API_BASE_URL=https://v0-lead-manager-app.vercel.app/api
BROWSER=chromium
HEADLESS=true
SLOW_MO=0
TIMEOUT=30000
```

### Pytest Configuration (`pytest.ini`)

```ini
[pytest]
testpaths = tests
addopts = -v --tb=short --html=reports/report.html
markers =
    ui: UI automation tests
    api: API tests
    smoke: Critical path tests
    regression: Full regression
    positive: Positive scenarios
    negative: Negative scenarios
```

---

## Debugging Guide

### Common Issues & Solutions

#### 1. Tests fail with "Element not found"

```bash
# Run with headed mode to see what's happening
./run.sh --ui --headed

# Or set in .env
HEADLESS=false
```

#### 2. API tests fail with 401 Unauthorized

```bash
# Verify credentials in config/settings.py
# Check if the API is accessible
curl -X POST https://v0-lead-manager-app.vercel.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"Admin@123"}'
```

#### 3. Playwright browsers not installed

```bash
source .venv/bin/activate
python -m playwright install chromium
```

#### 4. Import errors

```bash
# Ensure you're in the project root
cd /path/to/Osmos.ai

# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 5. Tests are slow

```bash
# Run in parallel
pytest -n auto

# Run only smoke tests
pytest -m smoke
```

### Debug Mode

```python
# Add breakpoint in test
import pdb; pdb.set_trace()

# Or use Playwright's pause
page.pause()  # Opens inspector
```

### Viewing Test Logs

```bash
# Run with full output
pytest -v -s --tb=long

# Save to file
pytest -v > test_output.log 2>&1
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: QA Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install chromium --with-deps
      
      - name: Run tests
        run: pytest --html=reports/report.html
      
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-reports
          path: reports/
```

---

## FAQ

### Q: How do I run tests for a specific user role?

```bash
# Tests are parameterized - run all role tests
pytest tests/api/test_auth_api_roles.py -v
pytest tests/ui/test_login_roles.py -v
```

### Q: How do I add a new test credential?

Edit `config/settings.py` and add to the `USERS` dictionary:

```python
UserRole.NEW_ROLE: UserCredentials(
    email="new@company.com",
    password="password",
    role=UserRole.NEW_ROLE,
    token="token",
    permissions=["view"]
)
```

### Q: How do I test a new form field?

1. Add method to `pages/create_lead_page.py`
2. Update `generate_lead_data()` in `utils/helpers.py`
3. Add test in `tests/ui/` or `tests/api/`

### Q: How do I generate Allure reports?

```bash
# Install Allure CLI (macOS)
brew install allure

# Run tests with Allure
pytest --alluredir=reports/allure-results

# View report
allure serve reports/allure-results
```

### Q: Tests pass locally but fail in CI?

- Ensure `HEADLESS=true` in CI
- Check network access to the test URL
- Verify all dependencies are installed
- Check for timing issues (add waits if needed)

---

## Test Coverage Summary

| Category | Tests | Description |
|----------|-------|-------------|
| Auth API - Basic | 9 | Login success, failures, validation |
| Auth API - Roles | 6 | All 3 roles + invalid credentials |
| Auth API - Security | 9 | SQL injection, XSS, long inputs |
| Leads API - CRUD | 17 | Create, read, all fields, validation |
| Leads API - Roles | 4 | Role-based access control |
| Leads API - Boundary | 12 | Edge cases, limits, special chars |
| Leads API - Security | 10 | Injection, auth bypass attempts |
| UI - E2E Flow | 9 | Login → Create → List → Logout |
| UI - Multi-Role | 7 | All roles login, badges, permissions |
| **Total** | **80+** | Comprehensive coverage |

---

## Tech Stack

| Tool | Version | Purpose |
|------|---------|--------|
| Python | 3.10+ | Language |
| Pytest | 8.x | Test framework |
| Playwright | 1.49+ | Browser automation |
| Requests | 2.32+ | HTTP/API testing |
| Allure | 2.13+ | Rich reporting |
| Faker | 33.x | Test data generation |
| pytest-html | 4.x | HTML reports |
| python-dotenv | 1.x | Environment config |
