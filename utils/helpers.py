import random
import string
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()

# Valid dropdown options from the UI (verified against screenshots and API)
VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
VALID_STATUSES = ["New", "Contacted", "Qualified", "Lost"]
VALID_SOURCES = ["Website", "Referral", "Cold Call", "LinkedIn", "Email Campaign", "Trade Show"]
VALID_INDUSTRIES = ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Education", "Other"]

# Common country calling codes for phone generation
COUNTRY_CODES = ["+1", "+44", "+91", "+61", "+49", "+33", "+81"]


def generate_valid_phone(include_country_code: bool = True) -> str:
    """Generate a valid phone number with optional country code.

    API accepts: digits, dashes, spaces, + symbol.
    Format: +1 555-234-5678

    Args:
        include_country_code: Whether to prefix with a country code (default: True).
    """
    area = fake.random_int(min=200, max=999)
    exchange = fake.random_int(min=200, max=999)
    number = fake.random_int(min=1000, max=9999)
    local = f"{area}-{exchange}-{number}"
    if include_country_code:
        code = random.choice(COUNTRY_CODES)
        return f"{code} {local}"
    return local


def generate_unique_email(prefix: str = "testlead") -> str:
    """Generate a unique email address for test data."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = "".join(random.choices(string.ascii_lowercase, k=4))
    return f"{prefix}_{timestamp}_{random_suffix}@testmail.com"


def generate_future_date(days_ahead: int = 30) -> str:
    """Generate a future date string in YYYY-MM-DD format."""
    future = datetime.now() + timedelta(days=random.randint(7, days_ahead))
    return future.strftime("%Y-%m-%d")


def generate_lead_data(overrides: dict = None) -> dict:
    """Generate realistic lead test data using Faker with ALL fields.

    Covers all fields from the Create Lead form:
    - Basic Information: Name, Email, Phone, Company, Job Title
    - Lead Classification: Industry, Source, Priority, Status
    - Deal Information: Deal Value, Expected Close Date, Follow-up Date
    - Additional Details: Lead is qualified, Email opt-in, Notes

    Args:
        overrides: Dictionary of fields to override in the generated data.

    Returns:
        Dictionary with all lead data fields.
    """
    data = {
        # Basic Information
        "name": fake.name(),
        "email": generate_unique_email(),
        "phone": fake.phone_number(),
        "company": fake.company(),
        "jobTitle": fake.job(),
        # Lead Classification
        "industry": random.choice(VALID_INDUSTRIES),
        "source": random.choice(VALID_SOURCES),
        "priority": random.choice(VALID_PRIORITIES),
        "status": random.choice(VALID_STATUSES),
        # Deal Information
        "dealValue": random.randint(10000, 200000),
        "expectedCloseDate": generate_future_date(90),
        "followUpDate": generate_future_date(14),
        # Additional Details
        "isQualified": random.choice([True, False]),
        "emailOptIn": random.choice([True, False]),
        "notes": fake.sentence(),
    }
    if overrides:
        data.update(overrides)
    return data


def generate_api_lead_payload(overrides: dict = None) -> dict:
    """Generate lead payload specifically for the API (matching API schema).

    Args:
        overrides: Dictionary of fields to override.

    Returns:
        Dictionary matching the API request body schema.
    """
    data = {
        "name": fake.name(),
        "email": generate_unique_email(),
        "phone": generate_valid_phone(),
        "company": fake.company(),
        "jobTitle": fake.job(),
        "industry": random.choice(VALID_INDUSTRIES),
        "source": random.choice(VALID_SOURCES),
        "priority": random.choice(VALID_PRIORITIES),
        "status": "New",
        "dealValue": random.randint(10000, 200000),
        "isQualified": False,
        "emailOptIn": False,
        "notes": fake.sentence(),
    }
    if overrides:
        data.update(overrides)
    return data


def generate_minimal_lead_payload() -> dict:
    """Generate minimal required lead payload (only name and email)."""
    return {
        "name": fake.name(),
        "email": generate_unique_email(),
    }


def generate_boundary_test_data() -> list:
    """Generate boundary test cases for lead fields."""
    return [
        {"field": "name", "value": "", "expected": "error", "reason": "Empty name"},
        {"field": "name", "value": "A", "expected": "success", "reason": "Single char name"},
        {"field": "name", "value": "A" * 255, "expected": "success_or_truncate", "reason": "Max length name"},
        {"field": "name", "value": "A" * 1000, "expected": "error_or_truncate", "reason": "Exceeds max length"},
        {"field": "email", "value": "", "expected": "error", "reason": "Empty email"},
        {"field": "email", "value": "invalid", "expected": "error", "reason": "Invalid email format"},
        {"field": "email", "value": "a@b.c", "expected": "success", "reason": "Minimal valid email"},
        {"field": "dealValue", "value": 0, "expected": "success", "reason": "Zero deal value"},
        {"field": "dealValue", "value": -1000, "expected": "error_or_success", "reason": "Negative deal value"},
        {"field": "dealValue", "value": 999999999, "expected": "success", "reason": "Large deal value"},
        {"field": "notes", "value": "A" * 5000, "expected": "success_or_truncate", "reason": "Very long notes"},
    ]


def generate_security_test_payloads() -> list:
    """Generate security-focused test payloads."""
    return [
        {"field": "name", "value": "<script>alert('xss')</script>", "attack": "XSS"},
        {"field": "name", "value": "'; DROP TABLE leads; --", "attack": "SQL Injection"},
        {"field": "email", "value": "test@test.com' OR '1'='1", "attack": "SQL Injection in email"},
        {"field": "notes", "value": "{{constructor.constructor('return this')()}}", "attack": "Prototype Pollution"},
        {"field": "name", "value": "../../../etc/passwd", "attack": "Path Traversal"},
        {"field": "notes", "value": "${7*7}", "attack": "Template Injection"},
        {"field": "company", "value": "Test\x00Company", "attack": "Null Byte Injection"},
    ]
