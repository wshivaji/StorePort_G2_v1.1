import pytest
from playwright.sync_api import Page, sync_playwright
from All_POM_Packages.video_review import VideoReview
from All_POM_Packages.login_page import LoginPage



@pytest.fixture
def setup(page: Page):
    video_review = VideoReview(page)
    yield video_review


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


def test_video_review(page: Page, setup):
    login_to_store_port(page)
    setup.click_video_review_config()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(4000)
    # setup.click_on_store()
    page.wait_for_timeout(20000)
    # setup.validate_filtered_store_data()
    setup.Ammount()
    page.wait_for_timeout(20000)



































