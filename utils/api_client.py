import requests
from typing import Any, Dict


class TodoAPIClient:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url.rstrip("/")

    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.api_base_url}/api/v1/users/register",
            json=user_data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.api_base_url}/api/v1/users/login",
            json={"email": email, "password": password},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def create_todo(self, token: str, item: str, is_completed: bool = False) -> Dict[str, Any]:
        response = requests.post(
            f"{self.api_base_url}/api/v1/tasks",
            json={"item": item, "isCompleted": is_completed},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_tasks(self, token: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.api_base_url}/api/v1/tasks",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def delete_task(self, token: str, task_id: str) -> None:
        response = requests.delete(
            f"{self.api_base_url}/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        response.raise_for_status()