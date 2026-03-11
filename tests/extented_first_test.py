import os
import re
import pytest

from faker import Faker
from dotenv import load_dotenv
from playwright.sync_api import Page, expect


load_dotenv()
faker = Faker()

BASE_URL = os.getenv("BASE_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def open_base_page(page: Page):
    """
    Navigate to the home page and assert the base title.

    Args:
        page (Page): Playwright Page instance.
    """
    page.goto(BASE_URL)
    expect(page).to_have_title(re.compile("Testomat"))

def open_login_page(page: Page):
    """
    Navigate to the login page from the base page.

    Args:
        page (Page): Playwright Page instance.
    """
    open_base_page(page)
    login_link = page.locator("#header").get_by_role("link", name="Log in")
    expect(login_link).to_be_visible()
    login_link.click()
    expect(page).to_have_title(re.compile("Testomat"))

def open_signup_page(page: Page):
    """
    Navigate to the signup page from the base page.

    Args:
        page (Page): Playwright Page instance.
    """
    open_base_page(page)
    sign_in_link = page.locator("#header").get_by_role("link", name="Start for free")
    expect(sign_in_link).to_be_visible()
    sign_in_link.click()
    expect(page).to_have_title(re.compile("Testomat"))

def login(page: Page, email: str, password: str):
    """
    Fill the login form and submit credentials.

    Args:
        page (Page): Playwright Page instance.
        email (str): Email address for login.
        password (str): Password for login.
    """
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign In").click()

def signup(page: Page, username: str, email: str, password: str, confirm_password: str):
    """
    Fill the signup form with typing delay and submit.

    Args:
        page (Page): Playwright Page instance.
        username (str): Desired username.
        email (str): Email address for registration.
        password (str): Account password.
        confirm_password (str): Password confirmation.
    """
    delay_ms = 100 # short typing delay, to avoid race conditions
    page.locator("#content-desktop #user_name").type(username, delay=delay_ms)
    page.locator("#content-desktop #user_email").type(email, delay=delay_ms)
    page.locator("#content-desktop #user_password").type(password, delay=delay_ms)
    page.locator("#content-desktop #user_password_confirmation").type(confirm_password, delay=delay_ms)
    page.locator("#content-desktop #terms").check()
    page.get_by_role("button", name="Sign Up").click()


@pytest.mark.parametrize("email, password, message", [
    pytest.param(faker.email(), faker.password(), "Invalid Email or password.", id="invalid_email_and_invalid_password"),
    pytest.param(EMAIL, faker.password(), "Invalid Email or password.", id="valid_email_and_invalid_password"),
    pytest.param(faker.email(), PASSWORD, "Invalid Email or password.", id="invalid_email_and_valid_password"),
    pytest.param(EMAIL, PASSWORD, "Signed in successfully", id="valid_email_and_valid_password"),
])
def test_login(page: Page, email: str, password: str, message: str):
    """
    Test login behavior with various email/password combinations.
    """
    open_login_page(page)
    login(page, email, password)
    expect(page.locator("#content-desktop").get_by_text(message)).to_be_visible()


@pytest.mark.parametrize("username, email, password, confirm_password, message", [
    pytest.param(faker.name(), EMAIL, "WrongPassword1!", "WrongPassword1!", "has already been taken", id="email_already_taken"),
    pytest.param(faker.name(), faker.email(), "WrongPass1!", "WrongPass1!", "is too short (minimum is 14 characters)", id="password_too_short"),
    pytest.param(faker.name(), faker.email(), "WRONGPASSWORD1!", "WRONGPASSWORD1!", "must contain at least 1 lowercase", id="password_doesnot_contain_uppercase"),
    pytest.param(faker.name(), faker.email(), "wrongpassword1!", "wrongpassword1!", "must contain at least 1 uppercase", id="password_doesnot_contain_lowercase"),
    pytest.param(faker.name(), faker.email(), "WrongPassword11", "WrongPassword11", "must contain special character", id="password_doesnot_contain_special_character"),
    pytest.param(faker.name(), faker.email(), "WrongPassword1!", "PasswordDoesNotMatch1!", "doesn't match Password", id="password_doesnot_match"),
])
def test_signup_validation_errors(page: Page, username: str, email: str, password: str, confirm_password: str, message: str):
    """
    Test signup behavior with various username/email/password combinations.
    """
    open_signup_page(page)
    signup(page, username, email, password=password, confirm_password=confirm_password)
    expect(page.locator("#content-desktop .text-red-500").get_by_text(message)).to_be_visible()