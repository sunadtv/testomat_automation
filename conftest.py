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

# Load environment variables from the .env file for test configuration
load_dotenv()


@pytest.fixture(scope="session")
def config() -> Config:
    """
    Provide application configuration for tests.
    The configuration values are loaded from environment variables defined in the `.env` file.
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
    """
    return Faker()


@pytest.fixture(scope="function")
def login(page: Page, config: Config):
    """
    Log in a valid user before running a test.
    This fixture navigates to the login page and authenticates using valid credentials from the test configuration.
    """
    open_login_page(page, config)
    login_user(page, config.email, config.password)