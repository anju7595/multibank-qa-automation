from playwright.sync_api import Page, expect
import re


class NavigationBar:
    def __init__(self, page: Page):
        self.page = page
        self.nav_container = page.locator("nav").first

        # Action Buttons (Sign In/Up)
        self.sign_in_btn = page.get_by_role("link", name=re.compile(r"Sign in", re.IGNORECASE))
        self.sign_up_btn = page.get_by_role("link", name=re.compile(r"Sign up", re.IGNORECASE))

        self.utility_icons = self.page.locator('[data-slot="popover-trigger"]')

    def get_link_by_name(self, name: str):
        return self.nav_container.get_by_role("link", name=re.compile(name, re.IGNORECASE)).first

    def verify_utility_icons(self):
        expect(self.utility_icons).to_have_count(2, timeout=10000)
        expect(self.utility_icons.nth(0)).to_be_visible()
        expect(self.utility_icons.nth(1)).to_be_visible()