from faker import Faker
from playwright.sync_api import Page

from core.config import Config
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage


def test_login_page(page: Page, config: Config, faker: Faker):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(config.email, faker.password())
