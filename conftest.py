import pytest
import os
from playwright.sync_api import sync_playwright


@pytest.fixture(params=["chromium", "firefox"])
def browser(request):
    """Launch browser with cross-browser support via parametrization."""
    with sync_playwright() as p:
        browser = getattr(p, request.param).launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Standard page fixture with a fresh context for each test."""
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures a screenshot on test failure.
    Includes a safety check to avoid KeyError if 'page' fixture isn't used.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Create reports directory if it doesn't exist
        if not os.path.exists("reports"):
            os.makedirs("reports")

        # Safely retrieve 'page' from the test's arguments
        page = item.funcargs.get("page")

        if page:
            screenshot_path = f"reports/{item.name}.png"
            page.screenshot(path=screenshot_path)