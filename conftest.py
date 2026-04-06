import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(params=["chromium", "firefox"])
def browser(request):
    with sync_playwright() as p:
        browser = getattr(p, request.param).launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs["page"]
        page.screenshot(path=f"reports/{item.name}.png")