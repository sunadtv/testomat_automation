from playwright.sync_api import Page


def select_company(page: Page, company_name: str):
    """
    Select a company from the company dropdown.
    """
    company = page.locator("#company_id")

    if company.locator("option:checked").inner_text() == company_name:
        return

    company.select_option(company_name)

def search_project(page: Page, project_name: str):
    """
    Search for a project using the dashboard search field.
    """
    page.locator("#content-desktop #search").fill(project_name)