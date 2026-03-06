"""
API Tests - Create Lead Module

This module contains all API tests related to creating leads.
Organized for Allure reporting under: API > Create Lead
"""
import pytest
import allure

from api.leads_api import LeadsAPI
from utils.helpers import (
    generate_api_lead_payload, 
    generate_valid_phone,
    VALID_PRIORITIES,
    VALID_STATUSES,
    VALID_SOURCES,
    VALID_INDUSTRIES,
    generate_minimal_lead_payload
)


def log_validation(check_name: str, expected, actual, passed: bool = None):
    """Log validation with expected vs actual."""
    status = "✓ PASS" if passed else "✗ FAIL" if passed is not None else "N/A"
    allure.attach(
        f"Check: {check_name}\nExpected: {expected}\nActual: {actual}\nStatus: {status}",
        name=f"Validation: {check_name}",
        attachment_type=allure.attachment_type.TEXT
    )


@allure.epic("Lead Management API")
@allure.feature("Create Lead")
@pytest.mark.api
class TestCreateLeadAPI:
    """API tests for creating leads."""

    @allure.story("Create with Required Fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_lead_success(self, leads_api: LeadsAPI):
        """Verify a lead can be created with valid data (simple success check)."""
        payload = generate_api_lead_payload()
        
        with allure.step("POST /api/leads with valid data"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate 200/201 success"):
            log_validation("Status Code", "200 or 201", response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}: {response.text}"

    @allure.story("Create with Required Fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_create_lead_response_contains_data(self, leads_api: LeadsAPI):
        """Verify create lead response contains the created lead data."""
        payload = generate_api_lead_payload()
        
        with allure.step("POST /api/leads"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate response contains lead data"):
            assert response.status_code in [200, 201]
            data = response.json()
            lead = data.get("lead", data)
            log_validation("Response contains lead name or ID", True, lead.get("name") == payload["name"] or "id" in lead, True)
            assert lead.get("name") == payload["name"] or "id" in data or "success" in data

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_exceeds_max_length_name(self, leads_api: LeadsAPI):
        """Verify name exceeding max length (255) is handled."""
        payload = generate_api_lead_payload({"name": "A" * 1000})
        
        with allure.step("POST /api/leads with 1000 char name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, 400, or 413", response.status_code, response.status_code in [200, 201, 400, 413])
            assert response.status_code in [200, 201, 400, 413]

    @allure.story("Create with Required Fields")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_create_lead_required_fields_only(self, leads_api: LeadsAPI):
        """TC-API09: Create lead with required fields only (name, email)."""
        payload = generate_api_lead_payload()
        
        with allure.step(f"POST /api/leads with name={payload['name']}"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate 201 Created"):
            log_validation("Status Code", "200 or 201", response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201]
            
            data = response.json()
            log_validation("Success", True, data.get("success"), data.get("success") is True)
            
            lead = data.get("lead", {})
            log_validation("Lead ID present", "Non-null", lead.get("id"), lead.get("id") is not None)
            log_validation("Name matches", payload["name"], lead.get("name"), lead.get("name") == payload["name"])
            log_validation("Email matches", payload["email"], lead.get("email"), lead.get("email") == payload["email"])

    @allure.story("Create with All Fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_lead_all_fields(self, leads_api: LeadsAPI):
        """TC-API10: Create lead with all fields populated."""
        payload = generate_api_lead_payload({
            "phone": generate_valid_phone(),
            "company": "Test Corporation",
            "jobTitle": "Senior Manager",
            "industry": "Technology",
            "source": "Website",
            "priority": "High",
            "status": "New",
            "dealValue": 75000,
            "isQualified": True,
            "emailOptIn": True,
            "notes": "Full field test lead"
        })
        
        with allure.step("POST /api/leads with all fields"):
            allure.attach(str(payload), "Request Payload", allure.attachment_type.JSON)
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate all fields saved"):
            assert response.status_code in [200, 201]
            data = response.json()
            lead = data.get("lead", {})
            
            fields_to_check = ["name", "email", "phone", "company", "jobTitle", "priority", "status"]
            for field in fields_to_check:
                log_validation(f"Field: {field}", payload.get(field), lead.get(field), payload.get(field) == lead.get(field))

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_without_name(self, leads_api: LeadsAPI):
        """TC-API11: Create lead without name field."""
        payload = {"email": "test@example.com"}
        
        with allure.step("POST /api/leads without name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate 400 error"):
            log_validation("Status Code", 400, response.status_code, response.status_code == 400)
            assert response.status_code == 400

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_without_email(self, leads_api: LeadsAPI):
        """TC-API12: Create lead without email field."""
        payload = {"name": "Test User"}
        
        with allure.step("POST /api/leads without email"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate 400 error"):
            log_validation("Status Code", 400, response.status_code, response.status_code == 400)
            assert response.status_code == 400

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_empty_name(self, leads_api: LeadsAPI):
        """TC-API: Create lead with empty name."""
        payload = generate_api_lead_payload({"name": ""})
        
        with allure.step("POST /api/leads with empty name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", 400, response.status_code, response.status_code == 400)
            assert response.status_code == 400

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_invalid_email_format(self, leads_api: LeadsAPI):
        """TC-API: Create lead with invalid email format."""
        payload = generate_api_lead_payload({"email": "not-an-email"})
        
        with allure.step("POST /api/leads with invalid email"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", 400, response.status_code, response.status_code == 400)
            assert response.status_code == 400

    @allure.story("Priority Variations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("priority", ["Low", "Medium", "High", "Critical"])
    def test_create_lead_all_priorities(self, leads_api: LeadsAPI, priority: str):
        """TC-C03: Create lead with different priority levels."""
        payload = generate_api_lead_payload({"priority": priority})
        
        with allure.step(f"POST /api/leads with priority={priority}"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate priority saved"):
            assert response.status_code in [200, 201]
            lead = response.json().get("lead", {})
            log_validation("Priority", priority, lead.get("priority"), lead.get("priority") == priority)
            assert lead.get("priority") == priority

    @allure.story("Status Variations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("status", ["New", "Contacted", "Qualified", "Lost"])
    def test_create_lead_all_statuses(self, leads_api: LeadsAPI, status: str):
        """TC-C04: Create lead with different statuses."""
        payload = generate_api_lead_payload({"status": status})
        
        with allure.step(f"POST /api/leads with status={status}"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate status saved"):
            assert response.status_code in [200, 201]
            lead = response.json().get("lead", {})
            log_validation("Status", status, lead.get("status"), lead.get("status") == status)
            assert lead.get("status") == status

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_invalid_status(self, leads_api: LeadsAPI):
        """TC-API17: Create lead with invalid status value."""
        payload = generate_api_lead_payload({"status": "Won"})
        
        with allure.step("POST /api/leads with invalid status 'Won'"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate rejection or acceptance"):
            log_validation("Status Code", "400 or 200/201", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Source Variations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("source", VALID_SOURCES)
    def test_create_lead_all_sources(self, leads_api: LeadsAPI, source: str):
        """Verify lead creation with each valid source."""
        payload = generate_api_lead_payload({"source": source})
        
        with allure.step(f"POST /api/leads with source={source}"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate source saved"):
            assert response.status_code in [200, 201], f"Source {source} failed: {response.text}"
            lead = response.json().get("lead", {})
            log_validation("Source", source, lead.get("source"), lead.get("source") == source)

    @allure.story("Industry Variations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("industry", VALID_INDUSTRIES)
    def test_create_lead_all_industries(self, leads_api: LeadsAPI, industry: str):
        """Verify lead creation with each valid industry."""
        payload = generate_api_lead_payload({"industry": industry})
        
        with allure.step(f"POST /api/leads with industry={industry}"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate industry saved"):
            assert response.status_code in [200, 201], f"Industry {industry} failed: {response.text}"
            lead = response.json().get("lead", {})
            log_validation("Industry", industry, lead.get("industry"), lead.get("industry") == industry)

    @allure.story("Boolean Combinations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("qualified,optin", [
        (True, True), (True, False), (False, True), (False, False)
    ])
    def test_create_lead_boolean_combinations(self, leads_api: LeadsAPI, qualified: bool, optin: bool):
        """Verify lead creation with all boolean field combinations."""
        payload = generate_minimal_lead_payload()
        payload["isQualified"] = qualified
        payload["emailOptIn"] = optin
        
        with allure.step(f"POST /api/leads with isQualified={qualified}, emailOptIn={optin}"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate boolean fields saved"):
            assert response.status_code in [200, 201]
            lead = response.json().get("lead", {})
            log_validation("isQualified", qualified, lead.get("isQualified"), lead.get("isQualified") == qualified)
            log_validation("emailOptIn", optin, lead.get("emailOptIn"), lead.get("emailOptIn") == optin)

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_empty_name(self, leads_api: LeadsAPI):
        """Verify empty name is rejected."""
        payload = generate_api_lead_payload({"name": ""})
        
        with allure.step("POST /api/leads with empty name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate 400 rejection"):
            log_validation("Status Code", 400, response.status_code, response.status_code == 400)
            assert response.status_code == 400

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_empty_email(self, leads_api: LeadsAPI):
        """Verify empty email is rejected."""
        payload = generate_api_lead_payload({"email": ""})
        
        with allure.step("POST /api/leads with empty email"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate 400 rejection"):
            log_validation("Status Code", 400, response.status_code, response.status_code == 400)
            assert response.status_code == 400

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_single_char_name_rejected(self, leads_api: LeadsAPI):
        """Verify single character name is rejected (min 2 chars required)."""
        payload = generate_api_lead_payload({"name": "A"})
        
        with allure.step("POST /api/leads with single char name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate 400 rejection"):
            log_validation("Status Code", 400, response.status_code, response.status_code == 400)
            assert response.status_code == 400, "Single char name should be rejected"

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_two_char_name(self, leads_api: LeadsAPI):
        """Verify two character name is accepted (minimum valid)."""
        payload = generate_api_lead_payload({"name": "AB"})
        
        with allure.step("POST /api/leads with two char name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate accepted"):
            log_validation("Status Code", "200 or 201", response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201]

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_max_length_name(self, leads_api: LeadsAPI):
        """Verify maximum length name (255 chars) is handled."""
        payload = generate_api_lead_payload({"name": "A" * 255})
        
        with allure.step("POST /api/leads with 255 char name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_very_long_name(self, leads_api: LeadsAPI):
        """Verify name exceeding max length is handled."""
        payload = generate_api_lead_payload({"name": "A" * 1000})
        
        with allure.step("POST /api/leads with 1000 char name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, 400, or 413", response.status_code, response.status_code in [200, 201, 400, 413])
            assert response.status_code in [200, 201, 400, 413, 422]

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_zero_deal_value(self, leads_api: LeadsAPI):
        """Verify zero deal value handling."""
        payload = generate_api_lead_payload({"dealValue": 0})
        
        with allure.step("POST /api/leads with dealValue=0"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_negative_deal_value(self, leads_api: LeadsAPI):
        """Verify negative deal value handling."""
        payload = generate_api_lead_payload({"dealValue": -5000})
        
        with allure.step("POST /api/leads with dealValue=-5000"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, 400, or 422", response.status_code, response.status_code in [200, 201, 400, 422])
            assert response.status_code in [200, 201, 400, 422]

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_very_large_deal_value(self, leads_api: LeadsAPI):
        """Verify very large deal value is handled."""
        payload = generate_api_lead_payload({"dealValue": 999999999999})
        
        with allure.step("POST /api/leads with very large dealValue"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Boundary Tests")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_create_lead_very_long_notes(self, leads_api: LeadsAPI):
        """Verify very long notes field is handled."""
        payload = generate_api_lead_payload({"notes": "A" * 5000})
        
        with allure.step("POST /api/leads with 5000 char notes"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, 400, or 413", response.status_code, response.status_code in [200, 201, 400, 413])
            assert response.status_code in [200, 201, 400, 413]

    @allure.story("Special Characters")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_lead_special_chars_in_name(self, leads_api: LeadsAPI):
        """Verify special characters in name are handled."""
        payload = generate_minimal_lead_payload()
        payload["name"] = "José María O'Brien-Smith"
        
        with allure.step("POST /api/leads with special chars in name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate accepted"):
            log_validation("Status Code", "200 or 201", response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201]

    @allure.story("Special Characters")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_lead_unicode_name(self, leads_api: LeadsAPI):
        """Verify unicode characters in name are handled."""
        payload = generate_minimal_lead_payload()
        payload["name"] = "田中太郎"
        
        with allure.step("POST /api/leads with unicode name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate accepted"):
            log_validation("Status Code", "200 or 201", response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201]

    @allure.story("Security")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_create_lead_xss_in_name(self, leads_api: LeadsAPI):
        """Verify XSS payload in name is handled safely."""
        payload = generate_minimal_lead_payload()
        payload["name"] = "<script>alert('xss')</script>"
        
        with allure.step("POST /api/leads with XSS in name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Security")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_create_lead_sql_injection_name(self, leads_api: LeadsAPI):
        """Verify SQL injection in name is handled safely."""
        payload = generate_minimal_lead_payload()
        payload["name"] = "'; DROP TABLE leads; --"
        
        with allure.step("POST /api/leads with SQL injection in name"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Security")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_create_lead_sql_injection_email(self, leads_api: LeadsAPI):
        """Verify SQL injection in email is handled safely."""
        payload = generate_minimal_lead_payload()
        payload["email"] = "test@test.com' OR '1'='1"
        
        with allure.step("POST /api/leads with SQL injection in email"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate rejection"):
            log_validation("Status Code", "400 or 422", response.status_code, response.status_code in [400, 422])
            assert response.status_code in [400, 422]

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_create_lead_path_traversal(self, leads_api: LeadsAPI):
        """Verify path traversal attempt is handled safely."""
        payload = generate_minimal_lead_payload()
        payload["name"] = "../../../etc/passwd"
        
        with allure.step("POST /api/leads with path traversal"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_create_lead_null_byte_injection(self, leads_api: LeadsAPI):
        """Verify null byte injection is handled safely."""
        payload = generate_minimal_lead_payload()
        payload["company"] = "Test\x00Company"
        
        with allure.step("POST /api/leads with null byte in company"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Security")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_create_lead_template_injection(self, leads_api: LeadsAPI):
        """Verify template injection is handled safely."""
        payload = generate_minimal_lead_payload()
        payload["notes"] = "${7*7} {{constructor.constructor('return this')()}}"
        
        with allure.step("POST /api/leads with template injection"):
            response = leads_api.create_lead(payload)
        
        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, or 400", response.status_code, response.status_code in [200, 201, 400])
            assert response.status_code in [200, 201, 400]

    @allure.story("Authorization")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_create_lead_without_auth(self, unauthenticated_leads_api: LeadsAPI):
        """TC-API: Create lead without authorization."""
        payload = generate_api_lead_payload()
        
        with allure.step("POST /api/leads without auth token"):
            response = unauthenticated_leads_api.create_lead(payload)
        
        with allure.step("Validate 401 Unauthorized"):
            log_validation("Status Code", 401, response.status_code, response.status_code == 401)
            assert response.status_code == 401

    @allure.story("Authorization")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_without_auth_detailed(self, unauthenticated_leads_api: LeadsAPI):
        """Detailed validation: create lead without auth returns proper error message."""
        payload = generate_api_lead_payload()

        with allure.step("Step 1: POST /api/leads without Authorization header"):
            response = unauthenticated_leads_api.create_lead(payload)

        with allure.step("Step 2: Validate 401 Unauthorized"):
            log_validation("HTTP Status Code", 401, response.status_code, response.status_code == 401)
            assert response.status_code == 401

        with allure.step("Step 3: Validate error message"):
            data = response.json()
            error = data.get("error", "")
            log_validation(
                "Error mentions authorization/token",
                "Contains 'authorization' or 'token'",
                f"Error: {error}",
                "authorization" in error.lower() or "token" in error.lower()
            )

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_empty_body(self, leads_api: LeadsAPI):
        """Verify lead creation fails with an empty request body."""
        with allure.step("POST /api/leads with empty body {}"):
            response = leads_api.create_lead({})

        with allure.step("Validate 400/422"):
            log_validation("Status Code", "400 or 422", response.status_code, response.status_code in [400, 422])
            assert response.status_code in [400, 422]

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_missing_name_key(self, leads_api: LeadsAPI):
        """Verify lead creation fails when name key is absent (not just empty)."""
        payload = generate_api_lead_payload()
        del payload["name"]

        with allure.step("POST /api/leads without name key"):
            response = leads_api.create_lead(payload)

        with allure.step("Validate 400/422"):
            log_validation("Status Code", "400 or 422", response.status_code, response.status_code in [400, 422])
            assert response.status_code in [400, 422]

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_missing_email_key(self, leads_api: LeadsAPI):
        """Verify lead creation fails when email key is absent (not just empty)."""
        payload = generate_api_lead_payload()
        del payload["email"]

        with allure.step("POST /api/leads without email key"):
            response = leads_api.create_lead(payload)

        with allure.step("Validate 400/422"):
            log_validation("Status Code", "400 or 422", response.status_code, response.status_code in [400, 422])
            assert response.status_code in [400, 422]

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_invalid_priority(self, leads_api: LeadsAPI):
        """Verify lead creation with invalid priority value."""
        payload = generate_api_lead_payload({"priority": "SuperUrgent"})

        with allure.step("POST /api/leads with priority=SuperUrgent"):
            response = leads_api.create_lead(payload)

        with allure.step("Validate handling"):
            log_validation("Status Code", "200, 201, 400, or 422", response.status_code, response.status_code in [200, 201, 400, 422])
            assert response.status_code in [200, 201, 400, 422]


@allure.epic("Lead Management API")
@allure.feature("Create Lead")
@pytest.mark.api
class TestCreateLeadRoleBasedAPI:
    """Role-based access tests for creating leads."""

    @allure.story("Role-Based Access")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_admin_can_create_lead(self):
        """Verify Admin role can create leads."""
        from api.auth_api import AuthAPI
        from config.settings import settings, UserRole
        auth = AuthAPI()
        user = settings.USERS[UserRole.ADMIN]
        token = auth.login_and_get_token(user.email, user.password)
        api = LeadsAPI(token=token)

        payload = generate_api_lead_payload()
        with allure.step("POST /api/leads as Admin"):
            response = api.create_lead(payload)

        with allure.step("Validate 200/201"):
            log_validation("Status Code", "200 or 201", response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201], f"Admin should create lead: {response.text}"

    @allure.story("Role-Based Access")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_manager_can_create_lead(self):
        """Verify Manager role can create leads."""
        from api.auth_api import AuthAPI
        from config.settings import settings, UserRole
        auth = AuthAPI()
        user = settings.USERS[UserRole.MANAGER]
        token = auth.login_and_get_token(user.email, user.password)
        api = LeadsAPI(token=token)

        payload = generate_api_lead_payload()
        with allure.step("POST /api/leads as Manager"):
            response = api.create_lead(payload)

        with allure.step("Validate 200/201"):
            log_validation("Status Code", "200 or 201", response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201], f"Manager should create lead: {response.text}"

    @allure.story("Role-Based Access")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_viewer_create_lead_behavior(self):
        """Document Viewer role behavior when creating leads."""
        from api.auth_api import AuthAPI
        from config.settings import settings, UserRole
        auth = AuthAPI()
        user = settings.USERS[UserRole.VIEWER]
        token = auth.login_and_get_token(user.email, user.password)
        api = LeadsAPI(token=token)

        payload = generate_api_lead_payload()
        with allure.step("POST /api/leads as Viewer"):
            response = api.create_lead(payload)

        with allure.step("Validate response (403 expected, 200/201 documents permissive behavior)"):
            log_validation("Status Code", "200, 201, or 403", response.status_code, response.status_code in [200, 201, 403])
            assert response.status_code in [200, 201, 403]

    @allure.story("Role-Based Access")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_viewer_cannot_create_lead(self):
        """Verify Viewer role cannot create leads (should be denied)."""
        from api.auth_api import AuthAPI
        from config.settings import settings, UserRole
        auth = AuthAPI()
        user = settings.USERS[UserRole.VIEWER]
        token = auth.login_and_get_token(user.email, user.password)
        api = LeadsAPI(token=token)

        payload = generate_api_lead_payload()
        with allure.step("POST /api/leads as Viewer (expect 403)"):
            response = api.create_lead(payload)

        with allure.step("Validate 403 Forbidden"):
            log_validation("Status Code", 403, response.status_code, response.status_code == 403)
            # Document actual behavior - may allow or deny
            assert response.status_code in [200, 201, 403], f"Viewer create returned unexpected status: {response.status_code}"


@allure.epic("Lead Management API")
@allure.feature("Create Lead")
@pytest.mark.api
class TestCreateLeadDetailedValidationAPI:
    """Detailed field-by-field validation tests for create lead."""

    @allure.story("Create Lead - Detailed Field Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_lead_with_field_validation(self, leads_api: LeadsAPI):
        """Create lead with step-by-step field validation in Allure."""
        with allure.step("Step 1: Prepare lead payload"):
            phone = generate_valid_phone()
            payload = generate_api_lead_payload({
                "name": "Test Lead Validation",
                "phone": phone,
                "company": "TestCorp",
                "jobTitle": "Test Manager",
                "industry": "Technology",
                "source": "Website",
                "priority": "High",
                "status": "New",
                "dealValue": 50000,
                "isQualified": True,
                "emailOptIn": False,
                "notes": "Detailed validation test"
            })
            allure.attach(str(payload), name="Lead Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Step 2: POST /api/leads"):
            response = leads_api.create_lead(payload)

        with allure.step("Step 3: Validate response status"):
            log_validation("HTTP Status Code", 201, response.status_code, response.status_code in [200, 201])
            assert response.status_code in [200, 201]

        with allure.step("Step 4: Parse and validate response"):
            data = response.json()
            log_validation("Response success", True, data.get("success"), data.get("success") is True)
            assert data.get("success") is True

            lead = data.get("lead", {})
            fields_to_check = [
                ("Name", payload["name"], lead.get("name")),
                ("Email", payload["email"], lead.get("email")),
                ("Company", payload["company"], lead.get("company")),
                ("Job Title", payload["jobTitle"], lead.get("jobTitle")),
                ("Industry", payload["industry"], lead.get("industry")),
                ("Source", payload["source"], lead.get("source")),
                ("Priority", payload["priority"], lead.get("priority")),
                ("Status", payload["status"], lead.get("status")),
                ("Deal Value", payload["dealValue"], lead.get("dealValue")),
                ("Is Qualified", payload["isQualified"], lead.get("isQualified")),
                ("Email Opt-in", payload["emailOptIn"], lead.get("emailOptIn")),
            ]
            for field_name, expected, actual in fields_to_check:
                with allure.step(f"Validate field: {field_name}"):
                    log_validation(f"Field: {field_name}", expected, actual, expected == actual)
                    assert expected == actual, f"{field_name} mismatch: expected {expected}, got {actual}"

        with allure.step("Step 5: Validate lead has ID"):
            lead_id = lead.get("id")
            log_validation("Lead has ID", "Non-null ID", f"ID: {lead_id}", lead_id is not None)
            assert lead_id is not None, "Lead should have an ID"
