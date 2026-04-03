from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email = "input[type='email']"
        self.password = "input[type='password']"
        self.login_btn = "button[type='submit']"

    def load(self):
        self.navigate("https://trade.multibank.io/")

    def login(self, email, password):
        self.fill(self.email, email)
        self.fill(self.password, password)
        self.click(self.login_btn)