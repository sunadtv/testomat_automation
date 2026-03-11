from playwright.sync_api import Page, expect


def test_login_with_invalid_credentials(page: Page):
    page.goto("https://testomat.io")

    expect(page).to_have_title("AI Test Management Tool | Testomat.io")
    expect(page.get_by_text("Log in", exact=True)).to_be_visible()

    page.get_by_role("link", name="Log in").click()
    expect(page).to_have_title("Testomat.io")

    page.locator("#content-desktop #user_email").fill("nonexistinguser@gmail.com")
    page.locator("#content-desktop #user_password").fill("wrongpassword")
    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
