import pytest

from faker import Faker
from playwright.sync_api import Page, expect

from utils.auth_utils import (
    open_login_page,
    open_signup_page,
    login_user,
    signup_user,
)

from core.config import Config


@pytest.mark.parametrize("email_type, password_type, message", [
    pytest.param("invalid", "invalid", "Invalid Email or password.", id="invalid_email_and_invalid_password"),
    pytest.param("valid", "invalid", "Invalid Email or password.", id="valid_email_and_invalid_password"),
    pytest.param("invalid", "valid", "Invalid Email or password.", id="invalid_email_and_valid_password"),
    pytest.param("valid", "valid", "Signed in successfully", id="valid_email_and_valid_password"),
])
def test_login(
    page: Page, config: Config, faker: Faker, 
    email_type: str, password_type: str, message: str
):
    """
    Test login behavior with various email/password combinations.
    """
    email = config.email if email_type == "valid" else faker.email()
    password = config.password if password_type == "valid" else faker.password()

    open_login_page(page, config)
    login_user(page, email, password)
    expect(page.locator("#content-desktop").get_by_text(message)).to_be_visible()


@pytest.mark.parametrize("email_type, password, confirm_password, message", [
    pytest.param("existing", "WrongPassword1!", "WrongPassword1!", "has already been taken", id="email_already_taken"),
    pytest.param("new", "WrongPass1!", "WrongPass1!", "is too short (minimum is 14 characters)", id="password_too_short"),
    pytest.param("new", "WRONGPASSWORD1!", "WRONGPASSWORD1!", "must contain at least 1 lowercase", id="password_doesnot_contain_uppercase"),
    pytest.param("new", "wrongpassword1!", "wrongpassword1!", "must contain at least 1 uppercase", id="password_doesnot_contain_lowercase"),
    pytest.param("new", "WrongPassword11", "WrongPassword11", "must contain special character", id="password_doesnot_contain_special_character"),
    pytest.param("new", "WrongPassword1!", "PasswordDoesNotMatch1!", "doesn't match Password", id="password_doesnot_match"),
])
def test_signup_validation_errors(
    page: Page, config: Config, faker: Faker,
    email_type: str, password: str, confirm_password: str, message: str
):
    """
    Test signup behavior with various username/email/password combinations.
    """
    username = faker.name()
    email = config.email if email_type == "existing" else faker.email()

    open_signup_page(page, config)
    signup_user(page, username, email, password=password, confirm_password=confirm_password)
    expect(page.locator("#content-desktop .text-red-500").get_by_text(message)).to_be_visible()