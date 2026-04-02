import allure
import pytest
from playwright.sync_api import expect

from pages.todo_page import TodoPage


@allure.feature("Todo UI")
@allure.story("API-created todo appears in UI")
@pytest.mark.smoke
def test_api_created_todo_is_visible_in_ui(authenticated_page, api_created_todo):
    todo_page = TodoPage(authenticated_page)

    with allure.step("Open todo page"):
        todo_page.goto()

    with allure.step("Verify API-created todo is visible"):
        todo_page.assert_todo_visible(api_created_todo["item"])


@allure.feature("Todo UI")
@allure.story("Todo count includes API-created record")
@pytest.mark.regression
def test_api_created_todo_row_exists(authenticated_page, api_created_todo):
    todo_page = TodoPage(authenticated_page)
    todo_page.goto()

    row = todo_page.get_todo_row_by_text(api_created_todo["item"])
    expect(row).to_be_visible()


@allure.feature("Todo UI")
@allure.story("User can delete an API-created todo")
@pytest.mark.regression
def test_user_can_delete_api_created_todo(authenticated_page, api_created_todo):
    todo_page = TodoPage(authenticated_page)
    todo_page.goto()

    todo_page.assert_todo_visible(api_created_todo["item"])
    todo_page.delete_todo(api_created_todo["item"])
    todo_page.assert_todo_deleted(api_created_todo["item"])

