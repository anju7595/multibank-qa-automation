from playwright.sync_api import Page

from pages import home_page
from pages.home_page import HomePage


def test_spot_trading_section(page: Page):
    home = HomePage(page)

    # 1. Navigate
    home.navigate("https://mb.io/en-AE")

    # ✅ Scroll BEFORE validation
    home.scroll_to_trading_section()

    # 2. Validate categories
    home.verify_trading_categories_visible()

    # 3. Validate structure
    home.verify_trading_pairs_structure()