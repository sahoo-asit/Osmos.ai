"""
UI Tests - Create Lead Module

This module contains all UI tests related to creating leads.
Organized for Allure reporting under: UI > Create Lead
"""
import pytest
import allure
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.leads_page import LeadsPage
from pages.create_lead_page import CreateLeadPage
from utils.helpers import generate_lead_data
from utils.ui_step_logger import DetailedStepLogger


@allure.epic("Lead Management UI")
@allure.feature("Create Lead")
@pytest.mark.ui
class TestCreateLeadUI:
    """UI tests for creating leads."""

    @allure.story("Create with Required Fields")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_create_lead_required_fields(self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage):
        """TC-C01: Create lead with required fields only (name, email)."""
        logger = DetailedStepLogger(page)
        lead_data = generate_lead_data()
        
        # Login
        logger.step("Login as admin")
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        # Open create dialog
        logger.step("Click Create Lead button")
        leads_page.click_create_lead()
        
        # Fill required fields
        logger.step("Enter lead name", f"Name: {lead_data['name']}")
        create_lead_page.fill_name(lead_data["name"])
        
        logger.step("Enter lead email", f"Email: {lead_data['email']}")
        create_lead_page.fill_email(lead_data["email"])
        
        # Submit
        logger.step("Click Create Lead to submit")
        create_lead_page.click_submit()
        
        # Wait for dialog to close
        logger.step("Wait for dialog to close")
        page.wait_for_selector("[role='dialog']", state="hidden", timeout=10000)
        
        # Wait for backend processing and refresh
        logger.step("Wait for lead to be saved")
        page.wait_for_timeout(3000)
        
        # Verify - clear search and wait
        logger.step("Clear search and look for created lead")
        search_input = page.locator("input[placeholder*='Search']")
        if search_input.is_visible():
            search_input.fill("")
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)
        
        # Search for the lead
        leads_page.search_leads(lead_data["name"])
        page.wait_for_timeout(2000)
        
        found = leads_page.is_lead_in_table(name=lead_data["name"])
        if not found:
            # Retry search once
            page.wait_for_timeout(2000)
            leads_page.search_leads(lead_data["name"])
            found = leads_page.is_lead_in_table(name=lead_data["name"])
        
        logger.verify("Lead appears in table", True, found, found)
        assert found, f"Lead {lead_data['name']} not found in table"

    @allure.story("Create with All Fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_create_lead_all_fields(self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage):
        """TC-C02: Create lead with all fields populated."""
        logger = DetailedStepLogger(page)
        lead_data = generate_lead_data()
        
        # Login
        logger.step("Login as admin")
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        # Open create dialog
        logger.step("Click Create Lead button")
        leads_page.click_create_lead()
        
        # Fill all fields
        logger.step("Enter name", f"Name: {lead_data['name']}")
        create_lead_page.fill_name(lead_data["name"])
        
        logger.step("Enter email", f"Email: {lead_data['email']}")
        create_lead_page.fill_email(lead_data["email"])
        
        logger.step("Enter phone", "Phone: 555-123-4567")
        create_lead_page.fill_phone("555-123-4567")
        
        logger.step("Enter company", "Company: Test Corp")
        create_lead_page.fill_company("Test Corp")
        
        logger.step("Select priority", "Priority: High")
        create_lead_page.select_priority("High")
        
        logger.step("Select status", "Status: New")
        create_lead_page.select_status("New")
        
        # Submit
        logger.step("Click Create Lead to submit")
        create_lead_page.click_submit()
        
        # Wait and verify
        logger.step("Wait for dialog to close")
        page.wait_for_selector("[role='dialog']", state="hidden", timeout=10000)
        
        leads_page.search_leads(lead_data["name"])
        found = leads_page.is_lead_in_table(name=lead_data["name"])
        logger.verify("Lead created with all fields", True, found, found)

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_empty_name(self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage):
        """TC-C05: Submit create lead form with empty name."""
        logger = DetailedStepLogger(page)
        
        # Login
        logger.step("Login as admin")
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        # Open create dialog
        logger.step("Click Create Lead button")
        leads_page.click_create_lead()
        
        # Fill only email
        logger.step("Leave name empty")
        
        logger.step("Enter email only", "Email: test@test.com")
        create_lead_page.fill_email("test@test.com")
        
        # Try to submit
        logger.step("Click Create Lead")
        create_lead_page.click_submit()
        
        # Dialog should still be open
        logger.step("Check dialog still open")
        page.wait_for_timeout(1000)
        
        dialog_visible = page.locator("[role='dialog']").is_visible()
        logger.verify("Dialog still open (validation failed)", True, dialog_visible, dialog_visible)

    @allure.story("Validation Errors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_empty_email(self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage):
        """TC-C06: Submit create lead form with empty email."""
        logger = DetailedStepLogger(page)
        
        # Login
        logger.step("Login as admin")
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        # Open create dialog
        logger.step("Click Create Lead button")
        leads_page.click_create_lead()
        
        # Fill only name
        logger.step("Enter name only", "Name: Test User")
        create_lead_page.fill_name("Test User")
        
        logger.step("Leave email empty")
        
        # Try to submit
        logger.step("Click Create Lead")
        create_lead_page.click_submit()
        
        # Dialog should still be open
        page.wait_for_timeout(1000)
        dialog_visible = page.locator("[role='dialog']").is_visible()
        logger.verify("Dialog still open (validation failed)", True, dialog_visible, dialog_visible)

    @allure.story("Dialog Behavior")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cancel_create_lead_dialog(self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage):
        """TC-C13: Cancel create lead dialog."""
        logger = DetailedStepLogger(page)
        
        # Login
        logger.step("Login as admin")
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        # Get initial count
        initial_count = leads_page.get_table_row_count()
        
        # Open create dialog
        logger.step("Click Create Lead button")
        leads_page.click_create_lead()
        
        # Fill some data
        logger.step("Enter some data")
        create_lead_page.fill_name("Should Not Be Created")
        create_lead_page.fill_email("shouldnot@test.com")
        
        # Cancel
        logger.step("Click Cancel or close dialog")
        # Try to close via X button or clicking outside
        close_btn = page.locator("[role='dialog'] button:has-text('Cancel'), [role='dialog'] [aria-label='Close']").first
        if close_btn.is_visible():
            close_btn.click()
        else:
            page.keyboard.press("Escape")
        
        page.wait_for_timeout(1000)
        
        # Verify no lead created
        final_count = leads_page.get_table_row_count()
        logger.verify("No lead created", initial_count, final_count, initial_count == final_count)

    @allure.story("Priority Variations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("priority", ["Low", "Medium", "High", "Critical"])
    def test_create_lead_with_priority(self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage, priority: str):
        """TC-C03: Create lead with different priority levels."""
        logger = DetailedStepLogger(page)
        lead_data = generate_lead_data()
        
        # Login
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        # Create lead with specific priority
        logger.step("Click Create Lead")
        leads_page.click_create_lead()
        
        logger.step(f"Fill form with priority={priority}")
        create_lead_page.fill_name(lead_data["name"])
        create_lead_page.fill_email(lead_data["email"])
        create_lead_page.select_priority(priority)
        
        logger.step("Submit")
        create_lead_page.click_submit()
        page.wait_for_selector("[role='dialog']", state="hidden", timeout=10000)
        
        # Verify
        leads_page.search_leads(lead_data["name"])
        found = leads_page.is_lead_in_table(name=lead_data["name"])
        logger.verify(f"Lead created with {priority} priority", True, found, found)

    @allure.story("Status Variations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("status", ["New", "Contacted", "Qualified", "Lost"])
    def test_create_lead_with_status(self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage, status: str):
        """TC-C04: Create lead with different statuses."""
        logger = DetailedStepLogger(page)
        lead_data = generate_lead_data()
        
        # Login
        login_page.open()
        page.locator("[type='email']").fill("admin@company.com")
        page.locator("[type='password']").fill("Admin@123")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/leads", timeout=10000)
        
        # Create lead with specific status
        logger.step("Click Create Lead")
        leads_page.click_create_lead()
        
        logger.step(f"Fill form with status={status}")
        create_lead_page.fill_name(lead_data["name"])
        create_lead_page.fill_email(lead_data["email"])
        create_lead_page.select_status(status)
        
        logger.step("Submit")
        create_lead_page.click_submit()
        page.wait_for_selector("[role='dialog']", state="hidden", timeout=10000)
        
        # Verify
        page.wait_for_timeout(3000)  # Wait for lead to appear in database
        leads_page.search_leads(lead_data["name"])
        page.wait_for_timeout(2000)
        found = leads_page.is_lead_in_table(name=lead_data["name"])
        if not found:
            # Retry once
            page.wait_for_timeout(2000)
            leads_page.search_leads(lead_data["name"])
            found = leads_page.is_lead_in_table(name=lead_data["name"])
        logger.verify(f"Lead created with {status} status", True, found, found)


@allure.epic("Lead Management UI")
@allure.feature("Create Lead - Detailed Steps")
@pytest.mark.ui
class TestCreateLeadDetailedSteps:
    """Create lead tests with detailed step-by-step logging."""

    @allure.story("Create Lead - Complete Detailed Workflow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_lead_complete_workflow(
        self, page: Page, login_page: LoginPage, leads_page: LeadsPage, create_lead_page: CreateLeadPage
    ):
        """
        Complete workflow to create a lead with detailed steps:
        a. Navigate to login page
        b. Enter credentials
        c. Login
        d. Wait for leads page
        e. Click Create Lead
        f. Fill lead form
        g. Submit form
        h. Verify lead created
        """
        logger = DetailedStepLogger(page)
        lead_data = generate_lead_data()
        
        # a. Navigate to login page
        logger.step(
            action="Navigate to login page",
            details="Opening https://v0-lead-manager-app.vercel.app/login",
            screenshot=True
        )
        login_page.open()
        
        # b. Enter credentials
        with allure.step("b. Enter login credentials"):
            logger.step(
                action="b1. Enter username",
                details="Username: admin@company.com",
                screenshot=False
            )
            page.locator("[type='email']").fill("admin@company.com")
            
            logger.step(
                action="b2. Enter password",
                details="Password: [MASKED]",
                screenshot=False
            )
            page.locator("[type='password']").fill("Admin@123")
        
        # c. Click Sign In
        logger.step(
            action="c. Click Sign In button",
            details="Submitting login form",
            screenshot=True
        )
        page.locator("button[type='submit']").click()
        
        # d. Wait for leads page
        logger.step(
            action="d. Wait for leads page to load",
            details="Expected URL: /leads",
            screenshot=True
        )
        page.wait_for_url("**/leads", timeout=10000)
        
        # e. Click Create Lead button
        logger.step(
            action="e. Click 'Create Lead' button",
            details="Opening create lead dialog",
            screenshot=True
        )
        leads_page.click_create_lead()
        
        # f. Fill lead form
        with allure.step("f. Fill lead form details"):
            logger.step(
                action="f1. Enter lead name",
                details=f"Name: {lead_data['name']}",
                screenshot=False
            )
            create_lead_page.fill_name(lead_data["name"])
            
            logger.step(
                action="f2. Enter lead email",
                details=f"Email: {lead_data['email']}",
                screenshot=False
            )
            create_lead_page.fill_email(lead_data["email"])
            
            logger.step(
                action="f3. Select priority",
                details="Priority: Medium",
                screenshot=False
            )
            create_lead_page.select_priority("Medium")
            
            logger.step(
                action="f4. Select status",
                details="Status: New",
                screenshot=True
            )
            create_lead_page.select_status("New")
        
        # g. Submit form
        logger.step(
            action="g. Click 'Create Lead' to submit form",
            details="Submitting new lead",
            screenshot=True
        )
        create_lead_page.click_submit()
        
        # h. Wait for dialog to close
        logger.step(
            action="h. Wait for dialog to close",
            details="Dialog should disappear",
            screenshot=True
        )
        create_lead_page.page.wait_for_selector("[role='dialog']", state="hidden", timeout=10000)
        
        # i. Verify lead appears in list
        logger.step(
            action="i. Search for created lead",
            details=f"Searching: {lead_data['name']}",
            screenshot=True
        )
        leads_page.search_leads(lead_data["name"])
        
        logger.verify(
            description="Lead appears in search results",
            expected=f"Lead '{lead_data['name']}' found in table",
            actual=f"Found: {leads_page.is_lead_in_table(name=lead_data['name'])}",
            passed=leads_page.is_lead_in_table(name=lead_data["name"])
        )

    @allure.story("Create Lead Dialog")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_lead_dialog_opens_and_closes(
        self, page: Page, login_page: LoginPage, leads_page: LeadsPage,
        create_lead_page: CreateLeadPage
    ):
        """Verify that the create lead dialog can be opened and closed properly."""
        from utils.allure_helpers import attach_screenshot
        
        with allure.step("Step 1: Login and open dialog"):
            login_page.open()
            login_page.login_as_admin()
            leads_page.wait_for_leads_page()
            leads_page.click_create_lead()
            create_lead_page.wait_for_dialog()
            attach_screenshot(page, "Dialog Opened")
            assert create_lead_page.is_dialog_open(), "Dialog should be open"

        with allure.step("Step 2: Verify dialog title"):
            title = create_lead_page.get_dialog_title()
            allure.attach(f"Dialog title: {title}", name="Dialog Title",
                          attachment_type=allure.attachment_type.TEXT)
            assert "Create" in title or "Lead" in title, f"Dialog title should contain 'Create' or 'Lead': {title}"

        with allure.step("Step 3: Close dialog and verify it closes"):
            create_lead_page.close_dialog()
            create_lead_page.page.wait_for_timeout(500)
            attach_screenshot(page, "Dialog Closed")
            assert not create_lead_page.is_dialog_open(), "Dialog should be closed after clicking X"

    @allure.story("Create Lead - Empty Required Fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_lead_with_empty_required_fields(
        self, page: Page, login_page: LoginPage, leads_page: LeadsPage,
        create_lead_page: CreateLeadPage
    ):
        """Verify submitting create lead form with empty required fields shows validation."""
        from utils.allure_helpers import attach_screenshot
        
        with allure.step("Step 1: Login and open create lead dialog"):
            login_page.open()
            login_page.login_as_admin()
            leads_page.wait_for_leads_page()
            leads_page.click_create_lead()
            create_lead_page.wait_for_dialog()
            attach_screenshot(page, "Empty Dialog")

        with allure.step("Step 2: Clear fields and submit"):
            create_lead_page.fill_name("")
            create_lead_page.fill_email("")
            create_lead_page.click_submit()
            create_lead_page.page.wait_for_timeout(1000)
            attach_screenshot(page, "After Empty Submit")

        with allure.step("Step 3: Verify dialog remains open (validation prevented submit)"):
            assert create_lead_page.is_dialog_open(), "Dialog should remain open on empty submit"
