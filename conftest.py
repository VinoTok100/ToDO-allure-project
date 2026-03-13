import os
import uuid
import pytest
from playwright.sync_api import Playwright

ARTIFACTS_DIR = "artifacts"
VIDEOS_DIR = os.path.join(ARTIFACTS_DIR, "videos")
TRACES_DIR = os.path.join(ARTIFACTS_DIR, "traces")

BASE_URL = "https://todo.qacart.com"
AUTH_DIR = ".auth"
AUTH_FILE = os.path.join(AUTH_DIR, "user.json")
#VIDEOS_DIR = "videos"


@pytest.fixture(scope="session")
def test_user(playwright: Playwright):
    api_context = playwright.request.new_context(base_url=BASE_URL)

    email = f"{uuid.uuid4()}@test.com"
    password = "Test1234"

    response = api_context.post(
        "/api/v1/users/register",
        data={
            "firstName": "Anthony",
            "lastName": "Tester",
            "email": email,
            "password": password,
        },
    )
    assert response.ok, f"Register failed: {response.text()}"

    body = response.json()

    user = {
        "email": email,
        "password": password,
        "token": body["access_token"],
    }

    api_context.dispose()
    return user


@pytest.fixture(scope="session")
def storage_state_file(playwright: Playwright, test_user: dict) -> str:
    os.makedirs(AUTH_DIR, exist_ok=True)

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()

    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded")
    page.get_by_test_id("email").fill(test_user["email"])
    page.get_by_test_id("password").fill(test_user["password"])
    page.get_by_role("button", name="LOGIN").click()

    page.wait_for_url(f"{BASE_URL}/todo")

    context.storage_state(path=AUTH_FILE)
    context.close()
    browser.close()

    return AUTH_FILE


@pytest.fixture
def authenticated_context(browser, storage_state_file, request):

    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(TRACES_DIR, exist_ok=True)

    #test_name = request.node.name
    test_name = request.node.name.replace("[", "_").replace("]", "")


    context = browser.new_context(
        base_url=BASE_URL,
        storage_state=storage_state_file,
        record_video_dir=VIDEOS_DIR,
        record_video_size={"width": 1280, "height": 720},
    )

    # START TRACE
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield context

    # STOP TRACE
    trace_path = os.path.join(TRACES_DIR, f"{test_name}.zip")
    context.tracing.stop(path=trace_path)

    context.close()

@pytest.fixture
def authenticated_page(authenticated_context):
    page = authenticated_context.new_page()
    yield page
    page.close()


@pytest.fixture
def api_created_todo(playwright: Playwright, test_user: dict):
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
    assert response.ok, f"Create todo failed: {response.text()}"

    body = response.json()
    api_context.dispose()

    return {
        "id": body["_id"],
        "item": todo_text,
        "response": body,
    }

#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--video",
#         action="store_true",
#         default=False,
#         help="Record Playwright videos",
#     )