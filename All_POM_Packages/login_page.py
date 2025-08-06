from playwright.sync_api import Page
from conftest import *


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open_login_page(self, url: str):
        self.page.goto(url)
        self.page.wait_for_timeout(8000)

    def fill_username(self, username: str):
        self.page.fill('//input[@name="username"]', username)
        self.page.wait_for_timeout(DELAY)

    def click_next(self):
        self.page.click('//input[@value="Next"]')
        self.page.wait_for_timeout(DELAY)

    def fill_password(self, password: str):
        self.page.fill('//input[@name="password"]', password)
        self.page.wait_for_timeout(DELAY)

    def click_sign_in(self):
        self.page.click('//input[@value="Sign In"]')
        self.page.wait_for_timeout(DELAY)

    def click_send_code(self):
        self.page.click('//input[@value="Send me the code"]')
        self.page.wait_for_timeout(DELAY)

    def wait_for_code_verification(self):
        self.page.wait_for_timeout(70000)

    # def confirm_sign_in(self):
    #     self.page.click('//input[@value="Sign In"]')
    #     self.page.wait_for_timeout(5000)

    def click_on_checkbox_enable_access_without_MFA_for_24_hours(self):
        self.page.get_by_text("Enable access without MFA for").click()
        self.page.wait_for_timeout(DELAY)

    def click_on_sign_in_button(self):
        self.page.get_by_role("button", name="Sign In").click()
        self.page.wait_for_timeout(5000)

    def get_store_port_g2_heading(self):
        text = self.page.get_by_text("StorePort G2").inner_text()
        self.page.wait_for_timeout(DELAY)
        return text


