from playwright.sync_api import Page
from conftest import *



class LoginPage:
    def __init__(self, page: Page):
        try:
            self.page = page
        except Exception as ex:
            print(type(ex).__name__)

    def open_login_page(self, url: str):
        try:
            self.page.goto(url)
            self.page.wait_for_timeout(8000)
        except Exception as ex:
            print(type(ex).__name__)

    def fill_username(self, username: str):
        try:
            self.page.fill('//input[@name="username"]', username)
            self.page.wait_for_timeout(DELAY)
        except Exception as ex:
            print(type(ex).__name__)

    def click_next(self):
        try:
            self.page.click('//input[@value="Next"]')
            self.page.wait_for_timeout(DELAY)
        except Exception as ex:
            print(type(ex).__name__)

    def fill_password(self, password: str):
        try:
            self.page.fill('//input[@name="password"]', password)
            self.page.wait_for_timeout(DELAY)
        except Exception as ex:
            print(type(ex).__name__)

    def click_sign_in(self):
        try:
            self.page.click('//input[@value="Sign In"]')
            self.page.wait_for_timeout(DELAY)
        except Exception as ex:
            print(type(ex).__name__)

    def click_send_code(self):
        try:
            self.page.click('//input[@value="Send me the code"]')
            self.page.wait_for_timeout(DELAY)
        except Exception as ex:
            print(type(ex).__name__)

    def wait_for_code_verification(self):
        try:
            self.page.wait_for_timeout(50000)
        except Exception as ex:
            print(type(ex).__name__)

    def click_on_checkbox_enable_access_without_MFA_for_24_hours(self):
        try:
            self.page.get_by_text("Enable access without MFA for").click()
            self.page.wait_for_timeout(DELAY)
        except Exception as ex:
            print(type(ex).__name__)

    def click_on_sign_in_button(self):
        try:
            self.page.get_by_role("button", name="Sign In").click()
            self.page.wait_for_timeout(5000)
        except Exception as ex:
            print(type(ex).__name__)

    def get_store_port_g2_heading(self):
        try:
            text = self.page.get_by_text("StorePort G2").inner_text()
            self.page.wait_for_timeout(DELAY)
            return text
        except Exception as ex:
            print(type(ex).__name__)



