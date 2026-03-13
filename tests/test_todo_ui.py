import allure
import pytest
from playwright.sync_api import expect
from pages.todo_page import TodoPage
#from pages  import   delete_page



@allure.feature("Todo UI")
@allure.story("API-created todo appears in UI")
@pytest.mark.smoke

def test_api_created_todo_is_visible_in_ui(authenticated_page, api_created_todo):
    todo_page = TodoPage(authenticated_page)

    with allure.step("Open todo page"):
        todo_page.goto()
        print("URL after goto:", authenticated_page.url)
        print("Local storage:", authenticated_page.evaluate("() => ({ ...localStorage })"))

    with allure.step("Verify API-created todo is visible"):
        todo_page.assert_todo_visible(api_created_todo["item"])


@allure.feature("Todo UI")
@allure.story("Todo count includes API-created record")
@pytest.mark.regression
def test_api_created_todo_row_exists(authenticated_page, api_created_todo):
    todo_page = TodoPage(authenticated_page)

    with allure.step("Open todo page"):
        todo_page.goto()

    with allure.step("Locate row for API-created todo"):
        row = todo_page.get_todo_row_by_text(api_created_todo["item"])
        expect(row).to_be_visible()


def test_delete_todo(authenticated_page, api_created_todo):
    todo_page = TodoPage(authenticated_page)

    todo_page.page.pause()
    todo_page.goto()

    todo_page.assert_todo_visible(api_created_todo["item"])

    todo_page.delete_todo(api_created_todo["item"])

    todo_page.assert_todo_deleted(api_created_todo["item"])