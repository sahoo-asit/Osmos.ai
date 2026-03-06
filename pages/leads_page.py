from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from config.settings import settings


class LeadsPage(BasePage):
    """Page object for the Leads listing page."""

    # Locators
    MAIN_CONTAINER = "[data-testid='leads-main']"
    CONTROLS_SECTION = "[data-testid='leads-controls']"
    SEARCH_INPUT = "[data-testid='leads-search-input']"
    STATUS_FILTER = "[data-testid='leads-status-filter']"
    EXPORT_BUTTON = "[data-testid='leads-export-btn']"
    CREATE_LEAD_BUTTON = "[data-testid='leads-create-new-btn']"
    TABLE_CONTAINER = "[data-testid='leads-table-container']"
    TABLE = "[data-testid='leads-table']"
    TABLE_HEADER_ROW = "[data-testid='leads-table-header-row']"
    TABLE_ROWS = "[data-testid='leads-table'] tbody tr"
    PAGINATION_INFO = "text=/Showing \\d+ to \\d+ of \\d+ leads/"
    NEXT_PAGE_BUTTON = "button:has-text('Next')"
    PREVIOUS_PAGE_BUTTON = "button:has-text('Previous')"
    LOGOUT_BUTTON = "button:has-text('Logout')"
    USER_EMAIL_DISPLAY = "text=admin@company.com"

    def open(self):
        """Navigate directly to the leads page."""
        self.navigate(settings.LEADS_URL)
        return self

    def wait_for_leads_page(self):
        """Wait until the leads page is fully loaded."""
        self.page.wait_for_selector(self.MAIN_CONTAINER, state="visible", timeout=15000)
        self.page.wait_for_selector(self.TABLE, state="visible", timeout=15000)
        return self

    def is_leads_page_displayed(self) -> bool:
        """Check if the leads page main container is visible."""
        return self.is_visible(self.MAIN_CONTAINER, timeout=10000)

    def click_create_lead(self):
        """Click the 'Create Lead' button to open the create lead dialog."""
        self.page.locator(self.CREATE_LEAD_BUTTON).click()
        return self

    def search_leads(self, search_term: str):
        """Search for leads using the search input.

        Args:
            search_term: Text to search by name, email, or phone.
        """
        search_input = self.page.locator(self.SEARCH_INPUT)
        search_input.clear()
        search_input.fill(search_term)
        self.page.wait_for_timeout(1000)
        return self

    def get_table_row_count(self) -> int:
        """Get the number of rows in the leads table."""
        self.page.wait_for_selector(self.TABLE_ROWS, state="visible", timeout=10000)
        return self.page.locator(self.TABLE_ROWS).count()

    def get_lead_names_from_table(self) -> list[str]:
        """Extract all lead names currently displayed in the table."""
        rows = self.page.locator(self.TABLE_ROWS)
        names = []
        for i in range(rows.count()):
            row_cells = rows.nth(i).locator("td")
            if row_cells.count() > 1:
                name = row_cells.nth(1).text_content() or ""
                names.append(name.strip())
        return names

    def get_lead_emails_from_table(self) -> list[str]:
        """Extract all lead emails currently displayed in the table."""
        rows = self.page.locator(self.TABLE_ROWS)
        emails = []
        for i in range(rows.count()):
            row_cells = rows.nth(i).locator("td")
            if row_cells.count() > 2:
                email = row_cells.nth(2).text_content() or ""
                emails.append(email.strip())
        return emails

    def is_lead_in_table(self, name: str = None, email: str = None) -> bool:
        """Check if a lead with the given name or email exists in the table.

        Args:
            name: Lead name to search for.
            email: Lead email to search for.

        Returns:
            True if the lead is found in the visible table rows.
        """
        if name:
            names = self.get_lead_names_from_table()
            if name in names:
                return True
        if email:
            emails = self.get_lead_emails_from_table()
            if email in emails:
                return True
        return False

    def filter_by_status(self, status: str):
        """Filter leads by status using the dropdown.

        Args:
            status: Status value (e.g., 'New', 'Contacted', 'Qualified').
        """
        self.page.locator(self.STATUS_FILTER).click()
        self.page.locator(f"[role='option']:has-text('{status}')").click()
        self.page.wait_for_timeout(1000)
        return self

    def click_export(self):
        """Click the Export button."""
        self.page.locator(self.EXPORT_BUTTON).click()
        return self

    def click_next_page(self):
        """Navigate to the next page of results."""
        self.page.locator(self.NEXT_PAGE_BUTTON).click()
        self.page.wait_for_timeout(1000)
        return self

    def click_logout(self):
        """Click the Logout button."""
        self.page.locator(self.LOGOUT_BUTTON).click()
        return self

    def get_pagination_text(self) -> str:
        """Get the pagination info text."""
        return self.page.locator(self.PAGINATION_INFO).text_content() or ""

    def get_total_leads_count(self) -> int:
        """Parse the total leads count from pagination info text."""
        text = self.get_pagination_text()
        # "Showing 1 to 10 of 20 leads"
        parts = text.split("of")
        if len(parts) > 1:
            count_str = parts[1].strip().split()[0]
            return int(count_str)
        return 0
