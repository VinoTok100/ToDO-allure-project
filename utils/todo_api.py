
from playwright.sync_api import APIRequestContext

class TodoAPI:
    def __init__(self, api_context: APIRequestContext):
        self.api_context = api_context

    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> dict:
        response = self.api_context.post(
            "/api/v1/users/register",
            data={
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "password": password,
            },
        )
        assert response.ok, f"Register failed: {response.text()}"
        return response.json()

    def create_todo(self, token: str, item: str) -> dict:
        response = self.api_context.post(
            "/api/v1/tasks",
            data={"item": item, "isCompleted": False},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.ok, f"Create todo failed: {response.text()}"
        return response.json()