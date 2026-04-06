import re
from playwright.sync_api import Page, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        # Centralized base URL for the project
        self.base_url = "https://mb.io/en-AE"

        # --- Locators ---
        self.header_nav = page.locator("header nav")
        self.nav_links = self.header_nav.locator("a")
        self.download_app_link = page.locator('a[data-button-type="download"]')
        self.mbg_link = page.get_by_role("link", name=re.compile(r"\$MBG", re.IGNORECASE))
        self.explore_tab = page.get_by_role("link", name="Explore", exact=True)

        # Trading Section Locators
        self.trading_section_titles = ["Top Gainers", "Trending Now", "Top Losers"]
        self.category_cards = page.locator("div").filter(
            has_text=re.compile(r"Top Gainers|Trending Now|Top Losers", re.IGNORECASE)
        )

    # --- Navigation Actions ---
    def navigate(self, url: str = None):
        """
        Navigates to the base URL by default, or a specific URL if provided.
        Switched to 'load' state to ensure cross-browser stability (Firefox fix).
        """
        target_url = url if url else self.base_url
        self.page.goto(target_url)
        # Using 'load' instead of 'networkidle' prevents non-deterministic timeouts in Firefox
        self.page.wait_for_load_state("load")

    def click_top_nav_item(self, name: str):
        nav_item = self.page.get_by_role("link", name=name).first
        expect(nav_item).to_be_visible(timeout=10000)
        nav_item.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_download_button(self):
        self.download_app_link.click(force=True)

    def click_mbg_token_link(self):
        self.mbg_link.click()

    def go_to_explore_section(self):
        self.explore_tab.click()

    # --- Trading Section Logic ---
    def scroll_to_trading_section(self):
        """Gradual scroll to handle lazy-loaded trading components."""
        for _ in range(3):
            self.page.mouse.wheel(0, 1000)
            self.page.wait_for_timeout(500)

        # Ensure the first category title is in the viewport
        first_title = self.page.get_by_text(self.trading_section_titles[0]).first
        if first_title.count() > 0:
            first_title.scroll_into_view_if_needed()

    def verify_trading_categories_visible(self):
        for title in self.trading_section_titles:
            expect(self.page.get_by_text(title)).to_be_visible(timeout=10000)

    def verify_trading_pairs_structure(self):
        """Validates the price and percentage format for top trading pairs."""
        for i in range(self.category_cards.count()):
            card = self.category_cards.nth(i)
            rows = card.locator("div").filter(has_text=re.compile(r"\$.*%", re.IGNORECASE))

            expect(rows.first).to_be_visible()

            for j in range(min(rows.count(), 5)):
                row_text = rows.nth(j).inner_text()

                has_price = re.search(r"\$[\d,]+(\.\d+)?", row_text)
                has_percent = re.search(r"(▲|▼)?\s*\d+(\.\d+)?%", row_text)

                assert has_price, f"Price format invalid in row: {row_text}"
                assert has_percent, f"Percentage format invalid in row: {row_text}"

    # --- Header & Footer Validation ---
    def get_top_nav_labels(self) -> list:
        self.nav_links.first.wait_for(state="visible")
        return [item.inner_text().strip() for item in self.nav_links.all()]

    def verify_download_link_attributes(self):
        expect(self.download_app_link).to_have_attribute("href", re.compile(r"mbio\.go\.link"))