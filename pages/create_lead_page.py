from pages.base_page import BasePage


class CreateLeadPage(BasePage):
    """Page object for the Create Lead dialog/modal.

    Form Fields (from screenshots):
    - Basic Information: Name*, Email*, Phone, Company, Job Title
    - Lead Classification: Industry, Source, Priority, Status
    - Deal Information: Deal Value ($), Expected Close Date, Follow-up Date
    - Additional Details: Lead is qualified (checkbox), Email opt-in (checkbox), Notes
    """

    # Dialog
    DIALOG = "[role='dialog']"
    DIALOG_TITLE = "[role='dialog'] h2, [role='dialog'] [data-slot='dialog-title']"
    CLOSE_BUTTON = "[role='dialog'] button:has(svg.lucide-x), [role='dialog'] button[aria-label='Close']"

    # Actions
    SUBMIT_BUTTON = "[role='dialog'] button[type='submit'], [role='dialog'] button:has-text('Create Lead')"
    CANCEL_BUTTON = "[role='dialog'] button:has-text('Cancel')"

    # Checkboxes
    QUALIFIED_CHECKBOX = "[role='dialog'] button[role='checkbox']:near(:text('qualified'))"
    EMAIL_OPTIN_CHECKBOX = "[role='dialog'] button[role='checkbox']:near(:text('email'))"

    # Textarea
    NOTES_TEXTAREA = "[role='dialog'] textarea"

    # Validation
    VALIDATION_ERROR = "[role='dialog'] p.text-destructive, [role='dialog'] [data-slot='form-message']"

    def _get_dialog(self):
        """Get the dialog locator."""
        return self.page.locator(self.DIALOG)

    def _get_input(self, index: int):
        """Get input field by index in the dialog."""
        return self._get_dialog().locator("input").nth(index)

    def wait_for_dialog(self):
        """Wait for the create lead dialog to appear."""
        self.page.wait_for_selector(self.DIALOG, state="visible", timeout=10000)
        return self

    def is_dialog_open(self) -> bool:
        """Check if the create lead dialog is visible."""
        return self.is_visible(self.DIALOG, timeout=5000)

    def get_dialog_title(self) -> str:
        """Get the title text of the dialog."""
        return self.page.locator(self.DIALOG_TITLE).first.text_content() or ""

    # === Basic Information Fields ===

    def fill_name(self, name: str):
        """Fill in the Name field (index 0)."""
        field = self._get_input(0)
        field.clear()
        field.fill(name)
        return self

    def fill_email(self, email: str):
        """Fill in the Email field (index 1)."""
        field = self._get_input(1)
        field.clear()
        field.fill(email)
        return self

    def fill_phone(self, phone: str):
        """Fill in the Phone field (index 2)."""
        field = self._get_input(2)
        field.clear()
        field.fill(phone)
        return self

    def fill_company(self, company: str):
        """Fill in the Company field (index 3)."""
        field = self._get_input(3)
        field.clear()
        field.fill(company)
        return self

    def fill_job_title(self, job_title: str):
        """Fill in the Job Title field (index 4)."""
        field = self._get_input(4)
        field.clear()
        field.fill(job_title)
        return self

    # === Deal Information Fields ===

    def fill_deal_value(self, value: str):
        """Fill in the Deal Value field (index 5)."""
        field = self._get_input(5)
        field.clear()
        field.fill(str(value))
        return self

    # === Additional Details ===

    def fill_notes(self, notes: str):
        """Fill in the Notes textarea."""
        field = self.page.locator(self.NOTES_TEXTAREA).first
        field.clear()
        field.fill(notes)
        return self

    def toggle_qualified(self, checked: bool = True):
        """Toggle the 'Lead is qualified' checkbox."""
        checkbox = self._get_dialog().locator("button[role='checkbox']").nth(0)
        current = checkbox.get_attribute("data-state") == "checked"
        if current != checked:
            checkbox.click()
        return self

    def toggle_email_optin(self, checked: bool = True):
        """Toggle the 'Opted in for email communications' checkbox."""
        checkbox = self._get_dialog().locator("button[role='checkbox']").nth(1)
        current = checkbox.get_attribute("data-state") == "checked"
        if current != checked:
            checkbox.click()
        return self

    # === Dropdown Selections ===

    def _select_dropdown(self, label_text: str, option_text: str):
        """Generic method to select a dropdown option by label."""
        dialog = self._get_dialog()
        # Find button near the label
        trigger = dialog.locator(f"button[role='combobox']:near(:text('{label_text}'))").first
        trigger.click()
        self.page.wait_for_timeout(300)
        self.page.locator(f"[role='option']:has-text('{option_text}')").click()
        return self

    def select_industry(self, industry: str):
        """Select industry from dropdown."""
        return self._select_dropdown("Industry", industry)

    def select_source(self, source: str):
        """Select source from dropdown."""
        return self._select_dropdown("Source", source)

    def select_priority(self, priority: str):
        """Select priority from dropdown (Low, Medium, High, Critical)."""
        return self._select_dropdown("Priority", priority)

    def select_status(self, status: str):
        """Select status from dropdown (New, Contacted, Qualified, Lost, Won)."""
        return self._select_dropdown("Status", status)

    # === Actions ===

    def click_submit(self):
        """Click the submit/Create Lead button."""
        self.page.locator(self.SUBMIT_BUTTON).first.click()
        return self

    def click_cancel(self):
        """Click the Cancel button."""
        self.page.locator(self.CANCEL_BUTTON).first.click()
        return self

    def close_dialog(self):
        """Close the dialog using the X button."""
        self.page.locator(self.CLOSE_BUTTON).first.click()
        return self

    # === High-Level Methods ===

    def create_lead(self, name: str, email: str, **kwargs):
        """Fill the create lead form and submit with required fields only.

        Args:
            name: Lead name (required).
            email: Lead email (required).
        """
        self.wait_for_dialog()
        self.fill_name(name)
        self.fill_email(email)
        self.click_submit()
        return self

    def create_lead_full(self, lead_data: dict):
        """Fill the create lead form with ALL fields and submit.

        Args:
            lead_data: Dictionary with all lead fields:
                - name, email (required)
                - phone, company, jobTitle (optional)
                - industry, source, priority, status (dropdowns)
                - dealValue (number)
                - isQualified, emailOptIn (booleans)
                - notes (text)
        """
        self.wait_for_dialog()

        # Required fields
        self.fill_name(lead_data["name"])
        self.fill_email(lead_data["email"])

        # Optional text fields
        if lead_data.get("phone"):
            self.fill_phone(lead_data["phone"])
        if lead_data.get("company"):
            self.fill_company(lead_data["company"])
        if lead_data.get("jobTitle"):
            self.fill_job_title(lead_data["jobTitle"])
        if lead_data.get("dealValue"):
            self.fill_deal_value(str(lead_data["dealValue"]))
        if lead_data.get("notes"):
            self.fill_notes(lead_data["notes"])

        # Checkboxes
        if lead_data.get("isQualified"):
            self.toggle_qualified(True)
        if lead_data.get("emailOptIn"):
            self.toggle_email_optin(True)

        self.click_submit()
        return self

    def get_validation_errors(self) -> list[str]:
        """Get all validation error messages displayed in the dialog."""
        errors = self.page.locator(self.VALIDATION_ERROR)
        return [errors.nth(i).text_content() or "" for i in range(errors.count())]

    def has_validation_errors(self) -> bool:
        """Check if any validation errors are displayed."""
        return self.page.locator(self.VALIDATION_ERROR).count() > 0
