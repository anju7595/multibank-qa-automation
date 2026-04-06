from playwright.sync_api import Page
from pages.home_page import HomePage

def test_spot_trading_section_visibility_and_structure(page: Page):
    """
    Validates that the Spot Trading section displays the correct categories
    and that trading pair data (Price/Percentage) follows the expected format.
    """
    home = HomePage(page)

    # 1. Navigate using the default base URL defined in the Page Object
    home.navigate()

    # 2. Scroll to the trading section to trigger lazy-loading of components
    home.scroll_to_trading_section()

    # 3. Validate that 'Top Gainers', 'Trending Now', and 'Top Losers' are visible
    home.verify_trading_categories_visible()

    # 4. Deep-dive validation of the trading pair data structure (Regex-based)
    home.verify_trading_pairs_structure()