from playwright.sync_api import Page, Locator, expect


class TodoPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_todo_input = page.get_by_test_id("new-todo")

    def goto(self) -> None:
        self.page.goto("/todo", wait_until="domcontentloaded")

    def get_todo_row_by_text(self, text: str) -> Locator:
        return self.page.locator('[data-testid="todo-item"]').filter(has_text=text)

    def get_delete_button_by_text(self, text: str) -> Locator:
        return self.get_todo_row_by_text(text).get_by_test_id("delete")

    def get_complete_checkbox_by_text(self, text: str) -> Locator:
        return self.get_todo_row_by_text(text).get_by_role("checkbox")

    def assert_todo_visible(self, text: str) -> None:
        expect(self.get_todo_row_by_text(text)).to_be_visible()

    def assert_todo_not_visible(self, text: str) -> None:
        expect(self.get_todo_row_by_text(text)).not_to_be_visible()

    def delete_todo(self, param):
        pass

    def assert_todo_deleted(self, param):
        pass