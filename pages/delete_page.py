from playwright.sync_api import Page, expect


class DeletePage:

    def __init__(self, page: Page):
        self.page = page

    def get_row_by_text(self, text: str):
        return self.page.locator('[data-testid="todo-item"]').filter(has_text=text)

    def get_delete_button(self, text: str):
        return self.get_row_by_text(text).get_by_test_id("delete")

    def delete_item(self, text: str):
        self.get_delete_button(text).click()

    def assert_deleted(self, text: str):
        expect(self.get_row_by_text(text)).not_to_be_visible()