from playwright.sync_api import sync_playwright
from All_POM_Packages.login_page import LoginPage
from conftest import *
from utilities import *


def test_open_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.open_login_page(store_port_login_url)
        # login_page.open_login_page('https://g2-cr-client-web-489921633482.us-central1.run.app/login')
        login_page.fill_username(EMAIL)
        # login_page.fill_username('manogna.maramreddy@facefirst.com')

        login_page.click_next()
        login_page.fill_password(PASSWORD)
        # login_page.fill_password('realize7Guard$Him')
        login_page.click_sign_in()
        login_page.click_send_code()
        login_page.click_on_checkbox_enable_access_without_MFA_for_24_hours()
        login_page.wait_for_code_verification()
        login_page.click_on_sign_in_button()
        text=login_page.get_store_port_g2_heading()
        print(text)
        # browser.close()
# open_url()
