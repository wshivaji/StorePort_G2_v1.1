import pytest
from playwright.sync_api import Page
from All_POM_Packages.user_creation_page import UserCreation
from All_POM_Packages.login_page import LoginPage
from conftest import *


@pytest.fixture
def setup(page: Page):
    user_creation = UserCreation(page)
    yield user_creation


def login_to_store_port(page: Page):
    try:
        login_page = LoginPage(page)
        login_page.open_login_page('https://g2-cr-client-web-489921633482.us-central1.run.app/login')
        login_page.fill_username('manogna.maramreddy@facefirst.com')
        login_page.click_next()
        login_page.fill_password('realize7Guard$Him')
        login_page.click_sign_in()
        login_page.click_send_code()
        login_page.click_on_checkbox_enable_access_without_MFA_for_24_hours()
        login_page.wait_for_code_verification()
        login_page.click_on_sign_in_button()
    except Exception as e:
        print(f"Login failed: {e}")
        raise


def test_click_user_management(page: Page):
    try:
        login_to_store_port(page)
        user_creation = UserCreation(page)
        user_creation.click_user_management()
        user_creation.click_on_add_user()
        user_creation.fill_first_name()
        user_creation.fill_last_name()
        user_creation.fill_email()
        user_creation.fill_company()
        user_creation.fill_country()
        user_creation.fill_role()
        user_creation.clicking_on_save()
        page.wait_for_timeout(5000)
    except Exception as ex:
        print(f"Test failed during user creation: {type(ex).__name__} - {str(ex)}")
        raise
