import re
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.why_multilink import WhyMultiLinkPage
from pages.explore_page import ExplorePage

def test_download_redirect_current_os(page: Page):
   """
   Checks where the 'Download' link takes a user based on their current OS.
   On your Windows machine, this will verify the Google Play Store.
   """
   page.goto("https://mb.io/en-AE")


   download_link = page.locator('a[data-button-type="download"]')


   # Catch the new tab
   with page.context.expect_page() as new_page_info:
       download_link.click(force=True)


   download_tab = new_page_info.value


   # Check if we are on Windows/Android or Mac/iOS
   current_url = download_tab.url


   if "play.google.com" in current_url:
       print("Detected Windows/Android redirect. Verifying Play Store...")
       expect(download_tab).to_have_url(re.compile(r"play\.google\.com"))
       assert "com.multibank.app" in current_url
   elif "apps.apple.com" in current_url:
       print("Detected Mac/iOS redirect. Verifying App Store...")
       expect(download_tab).to_have_url(re.compile(r"apps\.apple\.com"))
   else:
       pytest.fail(f"Unexpected redirection URL: {current_url}")


   download_tab.close()

# --- Test 2: Forced Mac Emulation (Verifies Apple Store link works) ---
def test_apple_store_link_via_mac_emulation(browser: Browser):
   """
   Specifically tricks the site into thinking we are on a Mac
   to ensure the Apple App Store link is functional.
   """
   # Create a 'fake' Mac environment
   mac_context = browser.new_context(
       user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
   )
   page = mac_context.new_page()
   page.goto("https://mb.io/en-AE")


   download_link = page.locator('a[data-button-type="download"]')


   with mac_context.expect_page() as new_page_info:
       download_link.click(force=True)

       apple_tab = new_page_info.value

       # Verify that the 'Adjust' tracking link correctly sent the 'Mac' user to Apple
       expect(apple_tab).to_have_url(re.compile(r"apps\.apple\.com"), timeout=15000)

       mac_context.close()


def test_mbg_about_navigation_flow(page: Page):
    home = HomePage(page)

    # 1. Start on the Sharjah/UAE landing page
    home.navigate("https://mb.io/en-AE")
    # 2. Identify the $MBG 🔥 link
    mbg_link = page.get_by_role("link", name=re.compile(r"\$MBG", re.IGNORECASE))

    # 3. Catch the second tab as it opens
    with page.context.expect_page() as new_page_info:
        mbg_link.click()

    mbg_tab = new_page_info.value

    # 4. Handle the secondary page navigation
    # Using "load" avoids the Firefox networkidle timeout we saw earlier
    mbg_tab.wait_for_load_state("load")

    # Click the 'About' span directly using text
    about_span = mbg_tab.locator("span").filter(has_text=re.compile(r"^About$", re.IGNORECASE)).first
    about_span.wait_for(state="visible", timeout=10000)
    about_span.click(force=True)

    # Verify content with our new manual scroll logic
    why_page = WhyMultiLinkPage(mbg_tab)
    why_page.verify_page_content()

    mbg_tab.close()

def test_explore_marketing_banner(page: Page):
    home = HomePage(page)

    # 1. Navigate to homepage
    home.navigate("https://mb.io/en-AE")

    # 2. Click Explore tab
    explore_tab = page.get_by_role("link", name="Explore", exact=True)
    explore_tab.click()

    # 3. Verify banner
    explore_page = ExplorePage(page)
    explore_page.verify_marketing_banner()