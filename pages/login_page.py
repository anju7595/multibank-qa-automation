from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Updated to use the 'name' attribute seen in your screenshot
        self.email = 'input[name="email"]'
        # Most login forms use type='password', but check if it's name="password" if this fails
        self.password = 'input[name="password"]'
        self.login_btn = "button[type='submit']"
        self.error_message = ".text-error"

    def load(self):
        # I noticed the URL in your code changed slightly from the error log
        self.navigate("https://trade.multibank.io/login")

    def login(self, email, password):
        self.fill(self.email, email)
        self.fill(self.password, password)
        self.click(self.login_btn)