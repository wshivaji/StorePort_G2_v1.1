from playwright.sync_api import Page
class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open_login_page(self, url: str):
        self.page.goto(url)
        self.page.wait_for_timeout(8000)

    def fill_username(self, username: str):
        self.page.fill('//input[@name="username"]', username)

    def click_next(self):
        self.page.click('//input[@value="Next"]')

    def fill_password(self, password: str):
        self.page.fill('//input[@name="password"]', password)

    def click_sign_in(self):
        self.page.click('//input[@value="Sign In"]')

    def click_send_code(self):
        self.page.click('//input[@value="Send me the code"]')

    def wait_for_code_verification(self):
        self.page.wait_for_timeout(70000)
    # def confirm_sign_in(self):
    #     self.page.click('//input[@value="Sign In"]')
    #     self.page.wait_for_timeout(5000)
