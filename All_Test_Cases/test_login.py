import pytest
from playwright.sync_api import sync_playwright
from All_POM_Packages.login_page import LoginPage
from conftest import *
import re


class TestLogin:
    @pytest.fixture(scope="function", autouse=True)
    def setup_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.login_page = LoginPage(self.page)
        self.login_page.open_login_page(store_port_login_url)
        yield
        self.browser.close()
        self.playwright.stop()
    #postive test case with valid username and password
    # def test_Login_to_StorePort_G2_TC01(self):
    #     self.login_page.fill_username(EMAIL)
    #     self.login_page.click_next()
    #     self.login_page.fill_password(PASSWORD)
    #     self.login_page.click_sign_in()
    #     self.login_page.click_send_code()
    #     self.login_page.click_on_checkbox_enable_access_without_MFA_for_24_hours()
    #     self.login_page.wait_for_code_verification()
    #     self.login_page.click_on_sign_in_button()
    #     text = self.login_page.get_store_port_g2_heading()
    #     print(text)
   # giving like empty email and click on next
   #  def test_Login_to_StorePort_G2_TC02(self):
   #      self.login_page.empty_email()
   #      self.login_page.click_next()
   #      assert self.page.locator('//span[@class="icon error-16"]//following-sibling::p').inner_text()
    # giving like empty password and click on next
    # def test_login_to_StorePort_G2_TC03(self):
    #     self.login_page.fill_username(EMAIL)
    #     self.login_page.click_next()
    #     self.login_page.empty_password()
    #     self.login_page.click_sign_in()
    #     assert self.page.locator('//span[@class="icon error-16"]//following-sibling::p').inner_text()
    # giving invalid email and valid password
    # def test_login_to_StorePort_G2_TC04(self):
    #     self.login_page.fill_username(invalid_email)
    #     self.login_page.click_next()
    #     self.login_page.fill_password(PASSWORD)
    #     self.login_page.click_sign_in()
    #     assert self.page.locator('//span[@class="icon error-16"]//following-sibling::p').inner_text()
    #clicking on reset password
    def test_login_to_StorePort_G2_TC05(self):
        self.page.get_by_role("link", name="Forgot password?").click()
        self.page.locator("#account-recovery-username").fill("s60191821@gmail.com")
        self.page.get_by_role("link", name="Reset via Email").click()
        self.page.wait_for_timeout(5000)
    #checking in email
    def test_checking_email(self):
        url="https://mail.google.com/mail/u/0/#inbox"
        self.page.goto(url)
        self.page.get_by_role("textbox", name="Email or phone").click()
        self.page.get_by_role("textbox", name="Email or phone").fill("s60191821@gmail.com")
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("textbox", name="Enter your password").click()
        self.page.get_by_role("textbox", name="Enter your password").fill("Maramreddy@12")
        self.page.get_by_role("button", name="Next").click()
        self.page.wait_for_timeout(5000)
        self.page.get_by_role("link", name="Account password reset  -").click()
        self.page.wait_for_timeout(5000)
        with self.page.expect_popup() as page1_info:
            self.page.get_by_role("link", name="Reset Password").click()
        self.page1 = page1_info.value
        self.page.wait_for_timeout(5000)
        self.page1.get_by_role("textbox", name="New password").click()
        self.page1.get_by_role("textbox", name="New password").fill("Akkiramreddy@12")
        self.page1.get_by_role("textbox", name="Repeat password").click()
        self.page1.get_by_role("textbox", name="Repeat password").fill("Akkiramreddy@12")
        self.page.wait_for_timeout(5000)
        self.page1.get_by_role("button", name="Reset Password").click()
        self.page1.get_by_role("button", name="Send me the code").click()
        self.page1.get_by_role("textbox", name="Verification code").click()
        self.page.wait_for_timeout(20000)
        self.page1.get_by_role("button", name="Verify").click()
        self.page.wait_for_timeout(20000)
    def test_opening_with_resetting_password(self):
        self.login_page.fill_username(S_Email)
        self.login_page.click_next()
        self.page.wait_for_timeout(5000)
        self.login_page.fill_password('Akkiramreddy@12')
        self.login_page.click_sign_in()
        self.page.get_by_role("button", name="Send me the code").click()
        self.page.get_by_role("textbox", name="Verification code").click()
        self.page.wait_for_timeout(20000)
        self.page.get_by_role("button", name="Sign In").click()
        self.page.wait_for_timeout(20000)
        self.page.locator("span").filter(has_text=re.compile(r"^s$")).click()
        assert self.page.get_by_role("menuitem", name="s s60191821@gmail.com").is_visible()





















































































































