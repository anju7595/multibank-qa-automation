import re
import pytest
from playwright.sync_api import Page, expect, Browser
from pages.home_page import HomePage
from pages.why_multilink import WhyMultiLinkPage
from pages.explore_page import ExplorePage


def test_download_redirect_logic(page: Page):
    """Validates dynamic redirection of the download button based on environment."""
    home = HomePage(page)
    home.navigate()

    with page.context.expect_page() as new_page_info:
        home.click_download_button()

    download_tab = new_page_info.value
    current_url = download_tab.url

    if "play.google.com" in current_url:
        expect(download_tab).to_have_url(re.compile(r"play\.google\.com"))
        assert "com.multibank.app" in current_url
    elif "apps.apple.com" in current_url:
        expect(download_tab).to_have_url(re.compile(r"apps\.apple\.com"))
    else:
        pytest.fail(f"Redirection failed. URL: {current_url}")


def test_apple_store_redirection_via_emulation(browser: Browser):
    """Verifies Apple Store link functionality using Mac OS user-agent emulation."""
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
    context = browser.new_context(user_agent=user_agent)
    page = context.new_page()

    home = HomePage(page)
    home.navigate()

    with context.expect_page() as new_page_info:
        home.click_download_button()

    apple_tab = new_page_info.value
    expect(apple_tab).to_have_url(re.compile(r"apps\.apple\.com"), timeout=15000)
    context.close()


def test_mbg_about_navigation_journey(page: Page):
    """Tests the navigation flow from the UAE landing page to the $MBG About section."""
    home = HomePage(page)
    home.navigate()

    with page.context.expect_page() as new_page_info:
        home.click_mbg_token_link()

    mbg_tab = new_page_info.value
    mbg_tab.wait_for_load_state("load")

    # Business action on the new tab
    about_section = mbg_tab.locator("span", has_text=re.compile(r"^About$", re.IGNORECASE)).first
    about_section.click(force=True)

    why_page = WhyMultiLinkPage(mbg_tab)
    why_page.verify_page_content()


def test_explore_marketing_banner_visibility(page: Page):
    """Ensures the marketing banner is rendered correctly on the Explore page."""
    home = HomePage(page)
    home.navigate()
    home.go_to_explore_section()

    explore_page = ExplorePage(page)
    explore_page.verify_marketing_banner()