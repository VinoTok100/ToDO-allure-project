from playwright.sync_api import Page, Locator, expect

class TodoPage:
    def __init__(self, page: Page):
        self.page = page
        self.todo_items = page.locator('[data-testid="todo-item"]')
        self.new_todo_input = page.get_by_test_id("new-todo")

    def goto(self) -> None:
        self.page.goto("/todo", wait_until="domcontentloaded")

    def get_todo_row_by_text(self, text: str) -> Locator:
        return self.todo_items.filter(has_text=text)

    def get_delete_button_by_text(self, text: str) -> Locator:
        return self.get_todo_row_by_text(text).get_by_test_id("delete")

    def assert_todo_visible(self, text: str) -> None:
        expect(self.get_todo_row_by_text(text)).to_be_visible()

    def assert_todo_deleted(self, text: str) -> None:
        expect(self.get_todo_row_by_text(text)).to_have_count(0)

    def delete_todo(self, text: str) -> None:
        self.get_delete_button_by_text(text).click()
        expect(self.get_todo_row_by_text(text)).to_have_count(0)