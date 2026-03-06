import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List
from dotenv import load_dotenv


def _load_env():
    """Load the correct .env file from config/env/ folder.

    Priority:
      1. --env=<name> command-line argument
      2. ENV environment variable
      3. Default: .env (lower environment)

    Env files are stored in config/env/:
      config/env/.env.lower    -> lower/dev environment
      config/env/.env.preprod  -> pre-production
      config/env/.env.prod     -> production

    Usage:
      pytest --env=preprod
      ENV=prod pytest
    """
    env_name = os.getenv("ENV", "lower")

    # Allow override via CLI: pytest --env=preprod
    for arg in sys.argv:
        if arg.startswith("--env="):
            env_name = arg.split("=", 1)[1]
            break

    # Env files are in config/env/ directory
    env_dir = os.path.join(os.path.dirname(__file__), "env")
    env_file = os.path.join(env_dir, f".env.{env_name}" if env_name != "lower" else ".env")

    # Fall back to .env if the specific file doesn't exist
    if not os.path.exists(env_file):
        env_file = os.path.join(env_dir, ".env")

    # Also try root .env as final fallback
    if not os.path.exists(env_file):
        env_file = ".env"

    load_dotenv(env_file, override=True)
    return env_name


ACTIVE_ENV = _load_env()


class UserRole(Enum):
    """User roles available in the Lead Manager application."""
    ADMIN = "admin"
    MANAGER = "manager"
    VIEWER = "viewer"


@dataclass
class UserCredentials:
    """User credentials with role-based permissions."""
    email: str
    password: str
    role: UserRole
    permissions: List[str]

    def can_create(self) -> bool:
        return "create" in self.permissions

    def can_edit(self) -> bool:
        return "edit" in self.permissions

    def can_delete(self) -> bool:
        return "delete" in self.permissions

    def can_export(self) -> bool:
        return "export" in self.permissions


class Settings:
    """Centralized configuration for the test framework.

    Supports multiple environments via .env files:
      .env         -> lower (default / dev-QA)
      .env.preprod -> pre-production
      .env.prod    -> production

    Switch environments:
      ENV=preprod pytest
      pytest --env=prod
    """

    # Active environment name (for logging/reporting)
    ENV: str = ACTIVE_ENV

    # Application URLs (loaded from env file)
    BASE_URL: str = os.getenv("BASE_URL", "https://v0-lead-manager-app.vercel.app")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://v0-lead-manager-app.vercel.app/api")

    # Browser Configuration
    BROWSER: str = os.getenv("BROWSER", "chromium")
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))

    # API Endpoints (derived from BASE_URL)
    @property
    def LOGIN_ENDPOINT(self) -> str:
        return f"{self.API_BASE_URL}/login"

    @property
    def LEADS_ENDPOINT(self) -> str:
        return f"{self.API_BASE_URL}/leads"

    @property
    def LOGIN_URL(self) -> str:
        return f"{self.BASE_URL}/login"

    @property
    def LEADS_URL(self) -> str:
        return f"{self.BASE_URL}/leads"

    # User Credentials - loaded from env file, with fallback defaults
    @property
    def USERS(self):
        return {
            UserRole.ADMIN: UserCredentials(
                email=os.getenv("ADMIN_EMAIL", "admin@company.com"),
                password=os.getenv("ADMIN_PASSWORD", "Admin@123"),
                role=UserRole.ADMIN,
                permissions=["create", "edit", "delete", "view", "export"]
            ),
            UserRole.MANAGER: UserCredentials(
                email=os.getenv("MANAGER_EMAIL", "qa@company.com"),
                password=os.getenv("MANAGER_PASSWORD", "password123"),
                role=UserRole.MANAGER,
                permissions=["create", "edit", "view", "export"]
            ),
            UserRole.VIEWER: UserCredentials(
                email=os.getenv("VIEWER_EMAIL", "tester@company.com"),
                password=os.getenv("VIEWER_PASSWORD", "Test@456"),
                role=UserRole.VIEWER,
                permissions=["view"]
            ),
        }

    # Invalid credentials for negative tests
    @property
    def INVALID_CREDENTIALS(self):
        admin_email = os.getenv("ADMIN_EMAIL", "admin@company.com")
        return [
            {"email": admin_email, "password": "wrongpass", "reason": "Wrong Password"},
            {"email": "unknown@test.com", "password": "password123", "reason": "Unregistered Email"},
            {"email": "notanemail", "password": "password123", "reason": "Invalid Email Format"},
            {"email": "", "password": "", "reason": "Empty Fields"},
        ]

    @property
    def ADMIN_EMAIL(self) -> str:
        return os.getenv("ADMIN_EMAIL", "admin@company.com")

    @property
    def ADMIN_PASSWORD(self) -> str:
        return os.getenv("ADMIN_PASSWORD", "Admin@123")

    def get_user(self, role: UserRole) -> UserCredentials:
        """Get user credentials by role."""
        return self.USERS[role]


settings = Settings()
