import pytest
import json
import re
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.navigation_bar import NavigationBar


# 1. Production-Grade Data Loader
def load_nav_data():
    """Resolves absolute path to JSON data to ensure cross-platform compatibility."""
    root_dir = Path(__file__).resolve().parent.parent
    data_path = root_dir / "data" / "navigation_data.json"

    if not data_path.exists():
        raise FileNotFoundError(f"CRITICAL: Test data missing at {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


config = load_nav_data()


# 2. Data-Driven Navigation Test---cp
@pytest.mark.parametrize("item", config["nav_items"])
def test_nav_links_functionality(page: Page, item):
   """
   Validates that primary navigation links (Explore, Features, etc.)
   reach the correct destinations, handling multi-tab redirects.
   """
   nav = NavigationBar(page)
   page.goto(config["base_url"])
   page.wait_for_load_state("domcontentloaded")


   nav_link = nav.get_link_by_name(item['name'])


   # Handle external domains (Token site) opening in new tabs
   if "token" in item['expected_url'] or "http" in item['expected_url']:
       with page.context.expect_page() as new_tab_info:
           nav_link.click(force=True)
       target_page = new_tab_info.value
   else:
       nav_link.click(force=True)
       target_page = page


   target_page.wait_for_load_state("load")
   expect(target_page).to_have_url(re.compile(item['expected_url'], re.IGNORECASE), timeout=15000)


# 3. New: Authentication and Utility Icon Test
def test_header_auth_and_utility_actions(page: Page):
    nav = NavigationBar(page)
    page.goto(config["base_url"])

    # 1. Handle potential Cookie Banner that blocks the header
    cookie_btn = page.get_by_role("button", name=re.compile(r"Accept|Allow|Agree", re.IGNORECASE))
    if cookie_btn.is_visible():
        cookie_btn.click()

    # 2. Verify Utility Icons
    nav.verify_utility_icons()

    # 3. Verify Auth Buttons
    expect(nav.sign_in_btn.first).to_be_visible()
    expect(nav.sign_up_btn.first).to_be_visible()