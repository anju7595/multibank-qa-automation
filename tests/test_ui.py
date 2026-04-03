from pages.login_page import LoginPage
from playwright.sync_api import expect
def test_login_page_ui_elements(page):
    page.goto("https://trade.multibank.io/")
    login_page = LoginPage(page)
    login_page.load()
    expect(login_page.email).to_be_visible()
    expect(login_page.password).to_be_visible()
    expect(login_page.login_button).to_be_visible()