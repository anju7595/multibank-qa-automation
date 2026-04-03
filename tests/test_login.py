from pages.login_page import LoginPage

def test_invalid_login(page):
    login_page = LoginPage(page)
    login_page.load()
    login_page.login("wrong@email.com", "wrongpass")

    assert "register" in page.url or login_page.is_error_visible()