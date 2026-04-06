import re
from playwright.sync_api import Page, expect


class ExplorePage:
    def __init__(self, page: Page):
        self.page = page

        # Banner elements
        self.banner_title = page.get_by_text(
            re.compile(r"Explore\.\s*Track\.\s*Trade\.", re.IGNORECASE)
        )

        self.banner_description = page.get_by_text(
            re.compile(r"real-time alerts", re.IGNORECASE)
        )

        self.download_button = page.get_by_role(
            "link", name=re.compile(r"Download the app", re.IGNORECASE)
        )

    def verify_marketing_banner(self):
        # Scroll to ensure visibility (important for lazy load)
        self.banner_title.scroll_into_view_if_needed()

        expect(self.banner_title).to_be_visible(timeout=10000)
        expect(self.banner_description).to_be_visible(timeout=10000)
        expect(self.download_button).to_be_visible(timeout=10000)

        print("Explore marketing banner verified successfully.")