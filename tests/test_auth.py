import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage


def test_successful_login(page):
    login_page = LoginPage(page)
    login_page.load()

    login_page.login("your_demo_user", "your_password")

    # Verification: Assert the URL or a dashboard element is visible
    expect(page).to_have_url("https://trade.multibank.io/dashboard")
    expect(login_page.profile_icon).to_be_visible()


def test_logout_flow(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("your_demo_user", "your_password")

    login_page.logout()

    # Verification: Ensure user is back at login page
    expect(login_page.login_button).to_be_visible()


@pytest.mark.parametrize("user, pwd, expected_error", [
    ("wrong_user", "valid_password", "Invalid credentials"),
    ("valid_user", "wrong_password", "Invalid credentials"),
    ("", "", "Required field")
])
def test_invalid_login_scenarios(page, user, pwd, expected_error):
    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login(user, pwd)

    # Verification: Check for error message text
    expect(login_page.error_message).to_contain_text(expected_error)