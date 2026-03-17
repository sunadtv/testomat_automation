from playwright.sync_api import Page, expect

### Get credentials from .env file ###
import os
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
### Get credentials from .env file ###


def test_login_with_invalid_credentials(page: Page):
    open_home_page(page)

    expect(page).to_have_title("AI Test Management Tool | Testomat.io")
    expect(page.get_by_text("Log in", exact=True)).to_be_visible()

    page.get_by_role("link", name="Log in").click()
    expect(page).to_have_title("Testomat.io")

    login_user(page, "nonexistinguser@gmail.com", "wrongpassword")

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()


def test_search_project_in_company(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, EMAIL, PASSWORD)

    target_project = "qa club"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_visible()

def test_should_be_possible_to_open_free_project(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, EMAIL, PASSWORD)

    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    target_project = "qa club"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible()


def open_home_page(page: Page):
    page.goto("https://testomat.io")

def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(EMAIL)
    page.locator("#content-desktop #user_password").fill(PASSWORD)
    page.get_by_role("button", name="Sign In").click()

def search_for_project(page: Page, target_project: str):
    page.locator("#content-desktop #search").fill(target_project)