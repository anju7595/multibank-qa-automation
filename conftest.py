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