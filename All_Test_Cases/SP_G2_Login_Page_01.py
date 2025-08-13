from conftest import *
from utilities import *
from playwright.sync_api import Page, expect
import pytest, playwright


def test_load_SP_01_login_page(page, credentials, delay, screenshot_path):
    try:
        log_in(page=page, username=conftest.EMAIL, password=conftest.PASSWORD, delay=conftest.DELAY)

    except Exception as ex:
        print(f'ex: {ex.__cause__}')


