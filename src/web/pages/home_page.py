from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("https://testomat.io")

    def is_loaded(self):
        header = self.page.locator("header")
        expect(header).to_be_visible()
        expect(header.get_by_role("link", name="Log in")).to_be_visible()
        expect(header.get_by_role("link", name="Start for free")).to_be_visible()

    def click_login(self):
        self.page.get_by_role("link", name="Log in").click()