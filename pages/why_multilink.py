from playwright.sync_api import Page, expect
import re


class WhyMultiLinkPage:
    def __init__(self, page: Page):
        self.page = page
        self.main_title = page.locator("h2, h1").filter(has_text=re.compile(r"Why MultiBank Group\?", re.IGNORECASE))
        self.show_more_btn = page.get_by_role("button", name=re.compile(r"Show more|Show less", re.IGNORECASE))

        # Use simple text locators without 'exact=True' to be more flexible
        self.liquidity_card = page.get_by_text("Substancial Liquidity")
        self.products_card = page.get_by_text("20,000+ Products")

    def verify_page_content(self):
        # 1. Reset the view to the top of the section
        self.main_title.first.scroll_into_view_if_needed()
        expect(self.main_title.first).to_be_visible(timeout=10000)

        # 2. Expand section
        if self.show_more_btn.is_visible():
            self.show_more_btn.click(force=True)
            # Give the UI 2 seconds to expand fully
            self.page.wait_for_timeout(2000)

        #  MANUAL SCROLL - Move the mouse wheel in small steps
        # This triggers lazy-loading without jumping to the bottom of the page
        for _ in range(5):
            self.page.mouse.wheel(0, 300)  # Scroll down 300 pixels
            self.page.wait_for_timeout(500)

        #  Verify visibility WITHOUT calling 'scroll_into_view' again
        expect(self.products_card.first).to_be_visible(timeout=10000)
        expect(self.liquidity_card.first).to_be_visible(timeout=10000)

        print("Successfully verified components with manual scroll control.")