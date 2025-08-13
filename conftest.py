import os
import pytest
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright
# from natsort import natsorted
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


store_port_login_url = "https://g2-cr-client-web-489921633482.us-central1.run.app/login"
FIRST_NAME = "core"
LAST_NAME = "user"
PASSWORD = "realize7Guard$Him"
EMAIL = "manogna.maramreddy@facefirst.com"
JOB_TITLE = "QA"
DEPARTMENT = "QA DEPT"
WORK_ADDRESS = "TEST WORK ADDRESS"
COUNTRY = ['Canada', 'Australia', 'United States']
ROLE = ['Admin - Full', 'Admin - Full (Engineering)', 'Customer Experience', 'Full Access (Engineering, except Admin)', 'Full Access except Admin', 'Sales', 'Sales + Tech Tools', 'Tech Services', 'Tech Services UK', 'Tech Services with User Admin', 'Theft Investigator', 'Tradeshow Demo User']
STORE_PERMISSIONS = ['Gatekeeper', '4 Way Market']

# BASE_URL = "https://10.0.1.36/"

# 1 letsencrypt, 2 ip, 3 go daddy

TIMEZONE = "(UTC+05:30) Chennai, Kolkata"

DELAY = 2000

USERS = [
    {
        "username": "itadmin",
        "role_id": "5. it system admin",
        "timezone": "Asia/Kolkata",
        "region": "scecore6-vm - KCORP"
    },
    {
        "username": "executive",
        "role_id": "1. executive",
        "timezone": "Asia/Kolkata",
        "region": "scecore6-vm - KCORP"
    },
    {
        "username": "operator",
        "role_id": "3. operator",
        "timezone": "Asia/Kolkata",
        "region": "Kroger San Fransisco - KSF"
    },
    {
        "username": "responder",
        "role_id": "4. responder",
        "timezone": "Asia/Kolkata",
        "region": "Kroger San Fransisco - KSF"
    },
    {
        "username": "approver",
        "role_id": "2. approver/supervisor",
        "timezone": "Asia/Kolkata",
        "region": "Kroger US West - USWEST"
    }

    # Add more users as needed
]


# USERS = [
#     {
#         "username": "itadmin",
#         "role_id": "5. it system admin",
#         "timezone": "Asia/Kolkata",
#         "region": "Kroger International - KCORP"
#     },
#     {
#         "username": "executive",
#         "role_id": "1. executive",
#         "timezone": "Asia/Kolkata",
#         "region": "Kroger International - KCORP"
#     },
#     {
#         "username": "operator",
#         "role_id": "3. operator",
#         "timezone": "Asia/Kolkata",
#         "region": "Kroger San Fransisco - KSF"
#     },
#     {
#         "username": "responder",
#         "role_id": "4. responder",
#         "timezone": "Asia/Kolkata",
#         "region": "Kroger San Fransisco - KSF"
#     },
#     {
#         "username": "approver",
#         "role_id": "2. approver/supervisor",
#         "timezone": "Asia/Kolkata",
#         "region": "Kroger US West - USWEST"
#     }
#
#     # Add more users as needed
# ]


NOTIFICATION_GROUPS = [
    {
        "name": "ng01",
        "user_ng": "responder responderF"
    }
    # Add more notification groups as needed
]

ENROLLMENT_GROUPS = [
    {
        "name": "abe",
        "color": "#EB8C00",
        "priority": "Medium",
        "eg_ng": "ng01 ng01_des Linked Unlinked 1"
    },
    {
        "name": "fraude",
        "color": "#00AEF0",
        "priority": "None",
        "eg_ng": "ng01 ng01_des Linked Unlinked 1"
    },
    {
        "name": "pte",
        "color": "#FFFC00",
        "priority": "Low",
        "eg_ng": "ng01 ng01_des Linked Unlinked 1"
    },
    {
        "name": "soe",
        "color": "#E0301E",
        "priority": "High",
        "eg_ng": "ng01 ng01_des Linked Unlinked 1"
    },
    {
        "name": "vipe",
        "color": "#FFFFFF",
        "priority": "None",
        "eg_ng": "ng01 ng01_des Linked Unlinked 1"
    }
    # Add more enrollment groups as needed
]

TAGS = [
    {
        "name": "ASSUALT",
        "serious_event": True
    },
    {
        "name": "THREAT",
        "serious_event": True
    },
    {
        "name": "PUSH CART",
        "serious_event": True
    },
    {
        "name": "FRAUD",
        "serious_event": False
    }
    # Add more tags as needed
]


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright):
    logger.info("Launching browser")
    # browser = playwright.chromium.launch(headless=False)
    # browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])  # Add --start-maximized argument
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    yield browser
    logger.info("Closing browser")
    browser.close()


@pytest.fixture(scope="session")
def context(browser):
    logger.info("Creating new browser context")
    context = browser.new_context(no_viewport=True, ignore_https_errors=True)
    yield context
    logger.info("Closing browser context")
    context.close()


@pytest.fixture(scope="function")
def page(context):
    logger.info("Creating new page")
    page = context.new_page()
    yield page
    logger.info("Closing page")
    page.close()


@pytest.fixture(scope="session")
def credentials():
    return {"username": FIRST_NAME, "password": PASSWORD, "email": EMAIL}


@pytest.fixture(scope="session")
def users():
    return USERS


@pytest.fixture(scope="session")
def notification_groups():
    return NOTIFICATION_GROUPS


@pytest.fixture(scope="session")
def enrollment_groups():
    return ENROLLMENT_GROUPS


@pytest.fixture(scope="session")
def tags():
    return TAGS


@pytest.fixture(scope="session")
def delay():
    return DELAY


@pytest.fixture(scope="session")
def screenshot_path():
    return f"{Path(__file__).parent}/screenshots/"
