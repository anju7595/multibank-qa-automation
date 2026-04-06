import pytest
import re
from playwright.sync_api import Page, expect
from pages.navigation_bar import NavigationBar
from utils.config import BASE_URL
from utils.config import load_nav_data

# Load configuration once for the module
config = load_nav_data()


@pytest.mark.parametrize("item", config.get("nav_items", []))
def test_navigation_menu_redirections(page: Page, item):
    """
    Validates primary navigation links across internal and external domains.
    Handles dynamic tab switching for external token sites.
    """
    nav = NavigationBar(page)
    nav.navigate()

    # Determine if we expect a new tab based on the test data
    is_external = item.get("is_external", False)

    if is_external:
        with page.context.expect_page() as new_tab_info:
            nav.click_link(item['name'])
        target_context = new_tab_info.value
    else:
        nav.click_link(item['name'])
        target_context = page

    # Verification with robust regex matching
    target_context.wait_for_load_state("load")
    expect(target_context).to_have_url(
        re.compile(item['expected_url'], re.IGNORECASE),
        timeout=15000
    )


def test_header_utility_and_auth_visibility(page: Page):
    """Verifies that essential utility icons and Auth buttons are present and visible."""
    nav = NavigationBar(page)
    nav.navigate()

    # Encapsulated logic: The Page Object handles the cookie banner internally
    nav.handle_cookie_banner()

    # UI Component Validation
    nav.verify_utility_icons()
    nav.verify_auth_buttons_presence()