from api.base_api import BaseAPI


class LeadsAPI(BaseAPI):
    """API client for lead management endpoints."""

    LEADS_ENDPOINT = "/leads"

    def get_leads(self, params: dict = None):
        """Fetch leads with optional pagination and filtering.

        Args:
            params: Query parameters (e.g., page, limit, status).

        Returns:
            Response object.
        """
        return self.get(self.LEADS_ENDPOINT, params=params)

    def get_lead_by_id(self, lead_id: int):
        """Fetch a specific lead by its ID.

        Args:
            lead_id: The ID of the lead.

        Returns:
            Response object.
        """
        return self.get(f"{self.LEADS_ENDPOINT}/{lead_id}")

    def create_lead(self, lead_data: dict):
        """Create a new lead.

        Args:
            lead_data: Dictionary containing lead fields
                       (name, email, priority, status, etc.).

        Returns:
            Response object.
        """
        return self.post(self.LEADS_ENDPOINT, json=lead_data)

    def update_lead(self, lead_id: int, lead_data: dict):
        """Update an existing lead.

        Args:
            lead_id: The ID of the lead to update.
            lead_data: Dictionary with fields to update.

        Returns:
            Response object.
        """
        return self.put(f"{self.LEADS_ENDPOINT}/{lead_id}", json=lead_data)

    def delete_lead(self, lead_id: int):
        """Delete a lead by its ID.

        Args:
            lead_id: The ID of the lead to delete.

        Returns:
            Response object.
        """
        return self.delete(f"{self.LEADS_ENDPOINT}/{lead_id}")
