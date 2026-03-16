import pytest

from playwright.sync_api import Page, expect

from utils.dashboard_utils import (
    select_company,
    search_project,
)


@pytest.mark.parametrize("company_name, has_projects", [
    pytest.param("QA Club Lviv", True, id="company_with_projects"),
    pytest.param("Free Projects", False, id="company_without_projects"),
])
def test_project_selection(
    page: Page, login,
    company_name: str, has_projects: bool
):
    """
    Verify project availability after selecting a company.
    """
    select_company(page, company_name)
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(visible=not has_projects)
    expect(page.get_by_role("link", name="Create project")).to_be_visible(visible=not has_projects)


@pytest.mark.parametrize("company_name, project_name, has_project", [
    pytest.param("QA Club Lviv", "industrial, movies", True, id="main_company_project_exists"),
    pytest.param("QA Club Lviv", "nonexistingproject", False, id="main_company_project_doesnot_exists"),
    pytest.param("Free Projects", "industrial, movies", False, id="free_project_doesnot_exists"),
    pytest.param("Free Projects", "nonexistingproject", False, id="free_project_doesnot_exists"),
])
def test_search_project_in_company(
    page: Page, login,
    company_name: str, project_name: str, has_project: bool
):
    """
    Verify project search results within a selected company.
    """
    select_company(page, company_name)
    search_project(page, project_name)
    expect(page.get_by_role("heading", name=project_name)).to_be_visible(visible=has_project)







