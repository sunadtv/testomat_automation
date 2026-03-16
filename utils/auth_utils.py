import re
from playwright.sync_api import Page, expect

from core.config import Config


def open_login_page(page: Page, config: Config):
    """
    Navigate to the login page.

    Args:
        page (Page): Playwright Page instance.
    """
    page.goto(config.login_url)
    expect(page).to_have_title(re.compile("Testomat"))

def open_signup_page(page: Page, config: Config):
    """
    Navigate to the signup page.

    Args:
        page (Page): Playwright Page instance.
    """
    page.goto(config.sign_up_url)
    expect(page).to_have_title(re.compile("Testomat"))

def login_user(page: Page, email: str, password: str):
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

def signup_user(page: Page, username: str, email: str, password: str, confirm_password: str):
    """
    Fill the signup form with typing delay and submit.

    Args:
        page (Page): Playwright Page instance.
        username (str): Desired username.
        email (str): Email address for registration.
        password (str): Account password.
        confirm_password (str): Password confirmation.
    """
    delay_ms = 50 # short typing delay, to avoid race conditions

    page.locator("#content-desktop #user_name").type(username, delay=delay_ms)
    page.locator("#content-desktop #user_email").type(email, delay=delay_ms)
    page.locator("#content-desktop #user_password").type(password, delay=delay_ms)
    page.locator("#content-desktop #user_password_confirmation").type(confirm_password, delay=delay_ms)

    page.locator("#content-desktop #terms").check()

    page.get_by_role("button", name="Sign Up").click()