from playwright.sync_api import sync_playwright
from All_POM_Packages.home_page import MainPage
import pytest


def test_click_user():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        main_page=MainPage(page)
        main_page.click_user_management()


