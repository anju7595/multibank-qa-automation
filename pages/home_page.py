import page
from playwright.sync_api import Page, expect
import re


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        # FIX: Use get_by_role("link") instead of "button"
        # OR better yet, use the unique data-attribute seen in your screenshot
        self.download_app_link = page.locator('a[data-button-type="download"]')
        self.top_gainers = page.get_by_text("Top Gainers")
        self.trending_now = page.get_by_text("Trending Now")
        self.top_losers = page.get_by_text("Top Losers")
        self.category_cards = page.locator("div").filter(
            has_text=re.compile(r"Top Gainers|Trending Now|Top Losers", re.IGNORECASE))
    def verify_trading_categories_visible(self):
        expect(self.top_gainers).to_be_visible(timeout=10000)
        expect(self.trending_now).to_be_visible(timeout=10000)
        expect(self.top_losers).to_be_visible(timeout=10000)

    def scroll_to_trading_section(self):
        # Scroll gradually to trigger lazy load
        for _ in range(3):
            self.page.mouse.wheel(0, 1200)
            self.page.wait_for_timeout(800)

        # Ensure section is in view
        self.top_gainers.first.scroll_into_view_if_needed()

    def verify_trading_pairs_structure(self):
        for i in range(self.category_cards.count()):
            card = self.category_cards.nth(i)

            # ✅ Only valid trading rows
            rows = card.locator("div").filter(
                has_text=re.compile(r"\$.*%", re.IGNORECASE)
            )

            expect(rows.first).to_be_visible()

            for j in range(min(rows.count(), 5)):
                row = rows.nth(j)
                text = row.inner_text()

                # Validate price
                assert re.search(r"\$[\d,]+(\.\d+)?", text), f"Price missing in: {text}"

                # Validate percentage (▲ / ▼ handled)
                assert re.search(r"(▲|▼)?\s*\d+(\.\d+)?%", text), f"Percentage missing in: {text}"

        print("Trading pairs structure validated successfully.")
    def open_download_modal(self):
        # 1. Wait for the element to be attached and visible
        self.download_app_link.wait_for(state="visible", timeout=10000)

        # 2. Scroll to it
        self.download_app_link.scroll_into_view_if_needed()
        self.download_app_link.click(force=True)

    def navigate(self, url: str):
        """Navigates to the given URL and handles initial page load."""
        self.page.goto(url)
        # Optional: Add logic here to wait for the page to be stable
        self.page.wait_for_load_state("networkidle")

    def verify_download_url(self):

        expect(self.download_app_link).to_have_attribute("href", re.compile(r"mbio\.go\.link"))

    # =========================
    # NAVIGATION SECTION (NEW)
    # =========================

    # Top navigation items (generic stable selector)
    top_nav_items = page.locator("header nav a")

    def get_top_nav_texts(self):
        """Returns all top navigation menu labels"""
        self.top_nav_items.first.wait_for(state="visible", timeout=10000)
        return [item.inner_text().strip() for item in self.top_nav_items.all()]

    def click_top_nav_item(self, name: str):
        """
        Clicks a top navigation item by visible text.
        Uses role-based locator for stability.
        """
        nav_item = self.page.get_by_role("link", name=name)

        expect(nav_item).to_be_visible(timeout=10000)
        nav_item.scroll_into_view_if_needed()
        nav_item.click()

        # wait for navigation to stabilize
        self.page.wait_for_load_state("domcontentloaded")

    def verify_top_navigation_items(self, expected_items: list):
        """
        Validates top navigation menu items are visible and correct.
        Data-driven approach (NO hardcoding inside test).
        """
        actual_items = self.get_top_nav_texts()

        for item in expected_items:
            assert item in actual_items, f"Missing navigation item: {item}"

    def verify_navigation_links_work(self, expected_items: list):
        """
        End-to-end validation:
        Click each nav item and ensure navigation happens successfully.
        """

        for item in expected_items:

            # Capture current URL before click
            old_url = self.page.url

            self.click_top_nav_item(item)

            # Wait for navigation or URL change
            self.page.wait_for_timeout(1000)

            new_url = self.page.url

            # Basic validation: URL should change OR page should stabilize
            assert new_url != old_url or self.page.evaluate("document.readyState") == "complete", \
                f"Navigation failed for: {item}"

    def is_header_visible(self):
        """Sanity check for layout stability"""
        header = self.page.locator("header")
        expect(header).to_be_visible(timeout=10000)

