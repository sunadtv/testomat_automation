import os
import pytest

from faker import Faker
from dotenv import load_dotenv
from playwright.sync_api import Page

from core.config import Config

from utils.auth_utils import (
    open_login_page,
    login_user,
)

load_dotenv()


@pytest.fixture(scope="session")
def config() -> Config:
    """
    Provide application configuration for tests.
    The configuration values are loaded from environment variables defined in the `.env` file.

    Scope:
        session – created once per test session.

    Returns:
        Config: Immutable configuration object containing:
            - base_app_url: Base URL of the application
            - login_url: Login page URL
            - sign_up_url: Sign-up page URL
            - email: Valid test user email
            - password: Valid test user password
    """
    base_app_url = os.getenv("BASE_APP_URL")

    return Config(
        base_app_url=base_app_url,
        login_url=f"{base_app_url}/users/sign_in",
        sign_up_url=f"{base_app_url}/users/sign_up",
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


@pytest.fixture(scope="session")
def faker() -> Faker:
    """
    Provide a shared Faker instance for generating random test data.

    Scope:
        session - a single Faker instance is reused across tests.

    Returns:
        Faker: Configured Faker generator.
    """
    return Faker()


@pytest.fixture(scope="function")
def login(page: Page, config: Config):
    open_login_page(page, config)
    login_user(page, config.email, config.password)