from playwright.sync_api import Page


def select_company(page: Page, company_name: str):
    """
    Select a company from the company dropdown.

    Args:
        page (Page): Playwright Page instance.
        company_name (str): Name of the company to select.
    """
    company = page.locator("#company_id")

    if company.locator("option:checked").inner_text() == company_name:
        return

    company.select_option(company_name)

def search_project(page: Page, project_name: str):
    """
    Search for a project using the dashboard search field.

    Args:
        page (Page): Playwright Page instance.
        project_name (str): Name of the project to search.
    """
    page.locator("#content-desktop #search").fill(project_name)