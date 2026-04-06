import re
from playwright.sync_api import Page, expect


class NavigationBar:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://mb.io/en-AE"

        # --- Locators ---
        self.nav_container = page.locator("nav").first

        # Action Buttons (Sign In/Up)
        self.sign_in_btn = page.get_by_role("link", name=re.compile(r"Sign in", re.IGNORECASE))
        self.sign_up_btn = page.get_by_role("link", name=re.compile(r"Sign up", re.IGNORECASE))

        # Utility Icons (Language/Region/Theme triggers)
        self.utility_icons = self.page.locator('[data-slot="popover-trigger"]')

        # Common overlays
        self.cookie_banner_btn = page.get_by_role("button", name=re.compile(r"Accept|Allow|Agree", re.IGNORECASE))

    # --- Navigation & Setup Actions ---
    def navigate(self):
        """Navigates to the base UAE URL and waits for the page to load."""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("load")

    def handle_cookie_banner(self):
        """
        Interacts with the cookie consent banner if present.
        Ensures that elements behind the overlay remain clickable.
        """
        if self.cookie_banner_btn.is_visible():
            self.cookie_banner_btn.click()

    # --- Interaction Methods ---
    def click_link(self, name: str):
        """
        Finds a navigation link by name and performs a forced click
        to bypass potential overlapping transparent elements.
        """
        link = self.nav_container.get_by_role("link", name=re.compile(name, re.IGNORECASE)).first
        expect(link).to_be_visible(timeout=10000)
        link.click(force=True)

    def get_link_by_name(self, name: str):
        """Returns the locator for a specific nav link for context-based tests."""
        return self.nav_container.get_by_role("link", name=re.compile(name, re.IGNORECASE)).first

    # --- Verification Methods ---
    def verify_utility_icons(self):
        """Validates that the expected global utility icons are rendered."""
        expect(self.utility_icons).to_have_count(2, timeout=10000)
        expect(self.utility_icons.nth(0)).to_be_visible()
        expect(self.utility_icons.nth(1)).to_be_visible()

    def verify_auth_buttons_presence(self):
        """Ensures both Sign In and Sign Up entry points are visible to the user."""
        expect(self.sign_in_btn.first).to_be_visible()
        expect(self.sign_up_btn.first).to_be_visible()