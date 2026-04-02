
from pathlib import Path
import os
import uuid
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://todo.qacart.com")
USER_PASSWORD = os.getenv("USER_PASSWORD", "Test1234")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

ARTIFACTS_DIR = Path("artifacts")
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"

AUTH_DIR = Path(".auth")
AUTH_FILE = AUTH_DIR / "user.json"


@pytest.fixture(scope="session")
def api_context(playwright: Playwright):
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def test_user(playwright: Playwright) -> dict:
    api_context = playwright.request.new_context(base_url=BASE_URL)

    email = f"{uuid.uuid4()}@test.com"

    response = api_context.post(
        "/api/v1/users/register",
        data={
            "firstName": "Anthony",
            "lastName": "Tester",
            "email": email,
            "password": USER_PASSWORD,
        },
    )
    assert response.ok, f"Register failed: {response.status} - {response.text()}"

    body = response.json()
    api_context.dispose()

    return {
        "email": email,
        "password": USER_PASSWORD,
        "token": body["access_token"],
    }
@pytest.fixture(scope="session")
def auth_storage_state(playwright: Playwright, test_user: dict) -> str:
    AUTH_DIR.mkdir(parents=True, exist_ok=True)

    browser = playwright.chromium.launch(headless=HEADLESS)
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()

    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded")
    page.get_by_test_id("email").fill(test_user["email"])
    page.get_by_test_id("password").fill(test_user["password"])
    page.get_by_role("button", name="LOGIN").click()
    page.wait_for_url(f"{BASE_URL}/todo")

    context.storage_state(path=str(AUTH_FILE))

    page.close()
    context.close()
    browser.close()

    return str(AUTH_FILE)


@pytest.fixture
def authenticated_context(browser, auth_storage_state, request):
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    TRACES_DIR.mkdir(parents=True, exist_ok=True)

    test_name = request.node.name.replace("[", "_").replace("]", "")

    context = browser.new_context(
        base_url=BASE_URL,
        storage_state=auth_storage_state,
        record_video_dir=str(VIDEOS_DIR),
        record_video_size={"width": 1280, "height": 720},
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield context

    trace_path = TRACES_DIR / f"{test_name}.zip"
    context.tracing.stop(path=str(trace_path))
    context.close()


@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    yield page
    page.close()


@pytest.fixture
def api_created_todo(playwright: Playwright, test_user: dict) -> dict:
    api_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Authorization": f"Bearer {test_user['token']}"
        },
    )

    todo_text = f"API Todo {uuid.uuid4().hex[:6]}"

    response = api_context.post(
        "/api/v1/tasks",
        data={
            "item": todo_text,
            "isCompleted": False,
        },
    )
    assert response.ok, f"Create todo failed: {response.status} - {response.text()}"

    body = response.json()
    api_context.dispose()


    return {
        "id": body["_id"],
        "item": todo_text,
        "response": body,
    }