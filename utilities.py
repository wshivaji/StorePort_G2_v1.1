import logging
import os
import pytest

from pathlib import Path
import conftest
from datetime import datetime

logger = logging.getLogger(__name__)


def log_in(page, username, password, delay):
    logger.info("Navigating to login page")
    page.goto(conftest.store_port_login_url)
    page.wait_for_timeout(delay)  # Explicit delay

    logger.info("Filling in username")
    if page.get_by_role("textbox", name="Email").is_visible():
        logger.info(f"Entering Username: {username}")
        page.get_by_role("textbox", name="Email").fill(username)
        logger.info("Filled Username")
    else:
        logger.warning("Username textbox not found")

    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Filling in password")
    if page.get_by_role("textbox", name="Password").is_visible():
        page.get_by_role("textbox", name="Password").fill(password)
        logger.info("Filled Password")
    else:
        logger.warning("Password textbox not found")

    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Clicking login button")
    page.get_by_role("button", name="Send me the code").click()
    page.wait_for_timeout(delay*2)  # Explicit delay
    page.get_by_role("textbox", name="Verification code").click()
    page.wait_for_timeout(delay*2)  # Explicit delay
    page.get_by_role("button", name="Sign In").click()

    page.wait_for_timeout(delay)  # Explicit delay


def agree_to_term(page, delay):
    logger.info("Agreeing to terms")
    if page.get_by_role("button", name="Click Here to Agree and").is_visible():
        logger.info("Agree button is visible")
        page.get_by_role("button", name="Click Here to Agree and").click()
        logger.info("Clicked Agree button")
        page.wait_for_timeout(delay)  # Explicit delay
    else:
        logger.warning("Agree button is not visible")


def log_out(page, delay):
    logger.info("Checking if logout button is visible")
    if page.get_by_text("Logout").is_visible():
        logger.info("Logout button is visible")
        page.get_by_text("Logout").click()
        logger.info("Clicked Logout button")
        page.wait_for_timeout(delay)  # Explicit delay
    else:
        logger.warning("Logout button is not visible")


def verify_duplicates(page, locate):
    # Fetch the list of existing users
    check_duplicates = page.query_selector_all(locate)
    existing_data = [element.inner_text() for element in check_duplicates]
    return existing_data


def fill_user_details(page, user, credentials, delay):
    logger.info("Filling in user details")

    page.get_by_role("textbox", name="Username", exact=True).fill(user["username"])
    logger.info("Filled Username")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_role("textbox", name="First Name").fill(user["username"] + "F")
    logger.info("Filled First Name")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_role("textbox", name="Last Name").fill(user["username"] + "L")
    logger.info("Filled Last Name")
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("select[name=\"userRoleId\"]").select_option(user["role_id"])
    logger.info("Selected User Role")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_role("textbox", name="New Password", exact=True).fill(credentials["password"])
    logger.info("Filled Password")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_role("textbox", name="Confirm Password").fill(credentials["password"])
    logger.info("Filled Confirm Password")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_text("Region Selection").click()
    logger.info("Clicked Region Selection")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_text(user["region"]).click()
    logger.info("Selected Region")
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("region-search").get_by_text("Save").click()
    logger.info("Clicked Save in Region Search")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_role("textbox", name="User Email").fill(user["username"] + "@facefirst.com")
    logger.info("Filled User Email")
    page.wait_for_timeout(delay)  # Explicit delay

    page.get_by_role("textbox", name="Alert Email").fill(user["username"] + "@facefirst.com")
    logger.info("Filled Alert Email")
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("select[name=\"timezoneID\"]").select_option(user["timezone"])
    logger.info("Selected Timezone")
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("a").filter(has_text="Save").click()
    logger.info("Clicked Save")
    page.wait_for_timeout(delay)  # Explicit delay


def create_user(page, user, credentials, delay):
    logger.info(f"Creating user: {user['username']}")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Create User", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    fill_user_details(page, user, credentials, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Verifying user creation")
    page.wait_for_timeout(delay)  # Explicit delay
    assert page.get_by_text("Success! A user has been created.").is_visible()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_2_user_creation_success_{user['username']}.png")
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing user creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(
        "li:nth-child(2) > .panel-div > .controller-panel-div > .panel-heading-container > .close-button-large"
    ).first.click()
    page.wait_for_timeout(delay)  # Explicit delay


def fill_store_group_details(page, store_group, delay):
    logger.info("Filling in store group details")
    page.get_by_role("textbox", name="Name").fill(store_group["name"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Description").fill(store_group["name"] + "_des")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Org Selection").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#tree-root div").filter(has_text=store_group["org"]).locator("i").nth(1).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("link", name="Save").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Save").first.click()
    page.wait_for_timeout(delay)  # Explicit delay


def create_store_group(page, store_group, delay):
    logger.info(f"Creating store group: {store_group['name']}")
    page.locator("a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Create Store Group", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    fill_store_group_details(page, store_group, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Verifying store group creation")
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_3_store_group_creation_success_{store_group['name']}.png")
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing store group creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(
        "li:nth-child(2) > .panel-div > .controller-panel-div > .panel-heading-container > .close-button-large"
    ).click()
    page.wait_for_timeout(delay)  # Explicit delay


def fill_additional_user_details(page, user, credentials, store_group, delay):
    logger.info("Filling in user details")
    page.get_by_role("textbox", name="Username", exact=True).fill(user["username"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="First Name").fill(user["username"] + "F")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Last Name").fill(user["username"] + "L")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("select[name=\"userRoleId\"]").select_option(user["role_id"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="New Password", exact=True).fill(credentials["password"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Confirm Password").fill(credentials["password"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Region Selection").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text(user["region"]).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("region-search").get_by_text("Save").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("select[name=\"storeGroupId\"]").select_option(store_group["name"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="User Email").fill(user["username"] + "@facefirst.com")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Alert Email").fill(user["username"] + "@facefirst.com")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("select[name=\"timezoneID\"]").select_option(user["timezone"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Save").click()
    page.wait_for_timeout(delay)  # Explicit delay


def create_additional_user(page, user, credentials, store_group, delay):
    logger.info(f"Creating additional user: {user['username']}")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Create User", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    fill_additional_user_details(page, user, credentials, store_group, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Verifying user creation")
    page.wait_for_timeout(delay)  # Explicit delay
    assert page.get_by_text("Success! A user has been created.").is_visible()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_4_additional_user_creation_success_{user['username']}.png")
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing user creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(
        "li:nth-child(2) > .panel-div > .controller-panel-div > .panel-heading-container > .close-button-large"
    ).first.click()
    page.wait_for_timeout(delay)  # Explicit delay


def fill_notification_group_details(page, ng, delay):
    logger.info("Filling in notification group details")
    page.get_by_role("textbox", name="Name", exact=True).fill(ng["name"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Description", exact=True).fill(ng["name"] + "_des")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Save").click()
    page.wait_for_timeout(delay)  # Explicit delay


def add_users_to_notification_group(page, ng, delay):
    logger.info("Adding users to notification group")
    page.get_by_role("button", name="Users").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#UserView a").filter(has_text="Filter").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Unlinked Users").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#UserView").get_by_role("listitem").filter(has_text=ng["user_ng"]).get_by_role("insertion").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#UserView a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Add User(s) to Alert").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_5_NG_creation_success_{ng['name']}_linking_user_{ng['user_ng']}.png")
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing notification group creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#UserView > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def create_notification_group(page, ng, delay):
    logger.info(f"Creating notification group: {ng['name']}")
    page.locator("a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Create Notification Group").click()
    page.wait_for_timeout(delay)  # Explicit delay
    fill_notification_group_details(page, ng, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    add_users_to_notification_group(page, ng, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing notification group creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("li:nth-child(2) > .panel-div > .controller-panel-div > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def fill_enrollment_group_details(page, eg, delay):
    logger.info("Filling in enrollment group details")
    page.get_by_role("textbox", name="Name").fill(eg["name"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Description").fill(eg["name"] + "_des")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"faceThreshold\"]").clear()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"faceThreshold\"]").fill("0.84")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"maskedFaceThreshold\"]").clear()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"maskedFaceThreshold\"]").fill("0.85")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("form[name=\"caseGroupForm\"] div").filter(has_text="Alert Color None Red Orange").locator(
        "#priority-select").select_option(eg["color"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("form[name=\"caseGroupForm\"] div").filter(has_text="Serious Offender High Medium").locator("#priority-select").select_option(eg["priority"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Save", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay


def add_notification_groups_to_enrollment_group(page, eg, delay):
    logger.info("Adding notification groups to enrollment group")
    page.get_by_role("button", name="Notification Groups").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#AlertGroupIndex a").filter(has_text="Filter").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Unlinked Notification Groups").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#AlertGroupIndex").get_by_role("listitem").filter(has_text=eg["eg_ng"]).get_by_role("insertion").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#AlertGroupIndex a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Add To Enrollment Groups").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_6_EG_creation_success_{eg['name']}_linking_user_{eg['eg_ng']}.png")
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing enrollment group creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#AlertGroupIndex > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def create_enrollment_group(page, eg, delay):
    logger.info(f"Creating enrollment group: {eg['name']}")
    page.locator("a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Create Enrollment Group").click()
    page.wait_for_timeout(delay)  # Explicit delay
    fill_enrollment_group_details(page, eg, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    add_notification_groups_to_enrollment_group(page, eg, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing enrollment group creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(".panel-div > .controller-panel-div > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def fill_tag_details(page, tag, delay):
    logger.info("Filling in tag details")
    page.get_by_role("textbox", name="Name", exact=True).fill(tag["name"])
    page.wait_for_timeout(delay)  # Explicit delay
    if tag["serious_event"]:
        page.locator("#tag-serious-event").check()
        page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Save", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay


def create_tag(page, tag, delay):
    logger.info(f"Creating tag: {tag['name']}")
    page.locator("a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Create Tag").click()
    page.wait_for_timeout(delay)  # Explicit delay
    fill_tag_details(page, tag, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_7_Tag_creation_success_{tag['name']}.png")
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info("Closing tag creation panel")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("li:nth-child(2) > .panel-div > .controller-panel-div > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def enroll_subject(page, subject, group, organization, index, delay):
    logger.info("Navigating to Identify & Enroll page")
    logger.info(f"Enrolling subject: {subject}")
    page.get_by_text("Identify & Enroll").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[type='file']").set_input_files(subject)
    page.wait_for_timeout(delay)  # Explicit delay

    identify_enroll_locator = page.locator("xpath=(//div[@class='ff-mobile-button posrel fltlft disblk tac'])[2]")
    identify_enroll_locator.click()
    page.wait_for_timeout(delay)  # Explicit delay

    error_msg = page.locator("xpath=(//p[@ng-bind='identifyErrorMessage'])[1]")
    if error_msg.text_content() == "Image quality too low. Face not found.":
        page.wait_for_timeout(delay)  # Explicit delay
        page.screenshot(path=f"screenshots/_8_subject_low_quality_{os.path.splitext(os.path.basename(subject))[0]}.png")
        page.wait_for_timeout(delay)  # Explicit delay
    else:
        try:
            text = page.inner_text("//div/p[contains(text(), 'Add Details')]")
            print(text)
            logger.info(f"Add Details text is visible")
            page.wait_for_timeout(delay)  # Explicit delay
        except Exception as e:
            logger.info(f"Add Details text is not visible")
            identify_enroll_locator = page.locator("div:nth-child(3) > .ff-mobile-bu-container > div:nth-child(2)")
            identify_enroll_locator.click()
            page.wait_for_timeout(delay)  # Explicit delay

        page.screenshot(path=f"screenshots/_8_subject_{os.path.splitext(os.path.basename(subject))[0]}_uploaded.png")
        page.wait_for_timeout(delay)  # Explicit delay

        page.locator("select[name=\"basis\"]").select_option("number:3")
        page.wait_for_timeout(delay)  # Explicit delay

        internal_group, spinbutton_value = group
        page.wait_for_timeout(delay)  # Explicit delay

        page.locator("select[name=\"internal_group\"]").select_option(internal_group)
        page.wait_for_timeout(delay)  # Explicit delay
        page.get_by_text("SELECT", exact=True).click()
        page.wait_for_timeout(delay)  # Explicit delay
        page.get_by_text(organization).click()
        page.wait_for_timeout(delay)  # Explicit delay
        page.locator("region-search").get_by_text("Save").click()
        page.wait_for_timeout(delay)  # Explicit delay
        page.locator("input[name=\"storeId\"]").click()
        page.wait_for_timeout(delay)  # Explicit delay
        page.locator("input[name=\"storeId\"]").fill(f"store_{os.path.splitext(os.path.basename(subject))[0]}_{internal_group.split(' ')[0].lower()}_{index + 1}")
        page.wait_for_timeout(delay)  # Explicit delay
        page.locator("input[name=\"enrollmentNumber\"]").fill(f"enroll_{os.path.splitext(os.path.basename(subject))[0]}_{internal_group.split(' ')[0].lower()}_{index + 1}")
        page.wait_for_timeout(delay)  # Explicit delay
        page.get_by_role("spinbutton").fill(spinbutton_value)
        page.wait_for_timeout(delay)  # Explicit delay

        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        page.locator("input[name='timeIncident']").fill(current_time)
        page.wait_for_timeout(delay)  # Explicit delay

        page.locator("input[name=\"action\"]").fill(f"action_{os.path.splitext(os.path.basename(subject))[0]}_{internal_group.split(' ')[0].lower()}_{index + 1}")
        page.wait_for_timeout(delay)  # Explicit delay
        page.get_by_text("SUBMIT REVIEW").click()
        page.wait_for_timeout(delay)  # Explicit delay

    page.locator(".panel-div > .controller-panel-div > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def filter_pending_review(page, delay):
    page.locator("a").filter(has_text="Filter").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Pending Review").click()
    page.wait_for_timeout(delay)  # Explicit delay


def approve_enrollments(page, delay):
    while not page.get_by_text("There are no enrollments matching the current search criteria or current filter.").is_visible():
        checkboxes = page.locator("li > .right-margin-menu > .right-menu-checkbox-container > .icheckbox_polaris > .iCheck-helper")
        page.wait_for_timeout(delay)  # Explicit delay
        for i in range(checkboxes.count()):
            checkboxes.nth(i).click()
            page.wait_for_timeout(500)  # Explicit delay
        page.locator("a").filter(has_text="Action").click()
        page.wait_for_timeout(delay)  # Explicit delay
        page.get_by_text("APPROVE Selected Enrollments").click()
        page.wait_for_timeout(delay)  # Explicit delay
        loadbutton = page.get_by_role("button", name="Load More")
        page.wait_for_timeout(delay)  # Explicit delay
        if loadbutton.is_visible():
            continue
        page.wait_for_timeout(delay)  # Explicit delay


def search_enrollment_group(page, eg, delay):
    page.locator("a").filter(has_text="Search").first.click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Enrollment Group Selection").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="filter enrollment group list").fill(eg["name"])
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#enrollmentGroup-selection-menu").get_by_role("checkbox").check()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Save").first.click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Search", exact=True).nth(2).click()
    page.wait_for_timeout(delay)  # Explicit delay


def add_tags_to_events(page, eg, delay):
    checkboxes = page.locator("li > .event-row > .right-margin-menu > .right-menu-checkbox-container")
    page.wait_for_timeout(delay)  # Explicit delay
    for j in range(checkboxes.count()):
        checkboxes.nth(j).click()
        page.wait_for_timeout(500)  # Brief delay to ensure click is registered
        if j == 5:
            break
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("a").filter(has_text="Action").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Edit Tags").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Filter").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("menu").get_by_text("Unlinked Tags").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("div:nth-child(5) > .right-menu-checkbox-container").first.click()
    page.wait_for_timeout(delay)  # Explicit delay

    if eg["name"] == "abe":
        page.locator("li:nth-child(2) > .right-margin-menu > .right-menu-checkbox-container").click()
        page.wait_for_timeout(delay)  # Explicit delay
    elif eg["name"] in ["fraude", "vipe"]:
        page.locator("li:nth-child(3) > .right-margin-menu > .right-menu-checkbox-container").click()
        page.wait_for_timeout(delay)  # Explicit delay
    elif eg["name"] == "pte":
        page.locator("li:nth-child(4) > .right-margin-menu > .right-menu-checkbox-container").click()
        page.wait_for_timeout(delay)  # Explicit delay
    elif eg["name"] == "soe":
        page.locator("li:nth-child(5) > .right-margin-menu > .right-menu-checkbox-container").click()
        page.wait_for_timeout(delay)  # Explicit delay

    page.locator("xpath=(//a[@class='btn dropdown-toggle pull-right toolbar-btn trigger-hide-search nav-pills-small'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Add Tag(s) to Selected Event(").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[2]").click()
    page.wait_for_timeout(delay)  # Explicit delay


def set_search_date_and_time(page, delay):
    page.locator("#includeStartDateEl").check()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#startDateField").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_title("Next Month").click()
    # Set the date
    # page.get_by_role("cell", name=conftest.search_date.strftime("%B %Y Toggle Date and")).click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.get_by_text(conftest.search_date.strftime("%b"), exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.get_by_role("cell", name=str(conftest.search_date.day)).nth(1).click()
    page.wait_for_timeout(delay)  # Explicit delay

    # Set the time
    page.get_by_title("Select Time").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_title("Pick Hour").click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.get_by_role("cell", name=conftest.search_time.strftime("%I")).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_title("Pick Minute").click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.get_by_role("cell", name=conftest.search_time.strftime("%M")).click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.get_by_role("button", name=conftest.search_time.strftime("%p")+" Toggle AM/PM").click()
    # toggle_am_pm = conftest.search_time.strftime("%p")
    # if conftest.search_time.strftime("%p") == "AM":
    #     page.get_by_title("Toggle Period").click()
    #     page.get_by_title("Toggle Period").click()
    # else:
    #     page.get_by_title("Toggle Period").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_title("Close the picker").click()
    page.wait_for_timeout(delay)  # Explicit delay


def select_organization(page, organization, delay):
    logger.info("Selecting organization")
    page.get_by_text("Org/Hierarchy Selection").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text(organization).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Save").click()
    page.wait_for_timeout(delay)  # Explicit delay


def submit_search(page, delay):
    logger.info("Submitting search")
    page.get_by_role("button", name="Submit Search").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.wait_for_selector("text=VISITOR SEARCH COMPLETE", state="visible")
    page.wait_for_timeout(delay)  # Explicit delay


def perform_visitor_image_search(page, subject, index, delay):
    logger.info(f"Visitor Image Subject: {subject}")
    page.get_by_text("Visitor Search", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[type='file']").set_input_files(subject)
    page.wait_for_timeout(delay)  # Explicit delay
    submit_search(page, delay)
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_11_vs_image_subject_{index + 1}_uploaded.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[2]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay


def perform_visitor_image_meta_search(page, subject, index, organization, delay):
    logger.info(f"Visitor Image Subject: {subject}")
    page.get_by_text("Visitor Search", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[type='file']").set_input_files(subject)
    page.wait_for_timeout(delay)  # Explicit delay
    set_search_date_and_time(page, delay)
    select_organization(page, organization, delay)
    page.get_by_role("combobox").select_option("string:15")
    page.wait_for_timeout(delay)  # Explicit delay
    submit_search(page, delay)
    page.screenshot(path=f"screenshots/_12_vs_image_meta_subject_{index + 1}_uploaded.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[2]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay


def enroll_mask_subject(page, subject, group, organization, delay):
    logger.info(f"Enrolling subject: {subject}")
    page.get_by_text("Identify & Enroll").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[type='file']").set_input_files(subject)
    page.wait_for_timeout(delay)  # Explicit delay

    identify_enroll_locator = page.locator("xpath=(//div[@class='ff-mobile-button posrel fltlft disblk tac'])[2]")
    identify_enroll_locator.click()
    page.wait_for_timeout(delay)  # Explicit delay

    try:
        text = page.inner_text("//div/p[contains(text(), 'Add Details')]")
        logger.info(f"Add Details text is visible")
        page.wait_for_timeout(delay)  # Explicit delay
    except Exception as e:
        logger.info(f"Add Details text is not visible")
        identify_enroll_locator = page.locator("div:nth-child(3) > .ff-mobile-bu-container > div:nth-child(2)")
        identify_enroll_locator.click()
        page.wait_for_timeout(delay)  # Explicit delay

    page.screenshot(path=f"screenshots/_14_subject_mask_uploaded.png")

    page.locator("select[name=\"basis\"]").select_option("number:3")
    page.wait_for_timeout(delay)  # Explicit delay

    internal_group, spinbutton_value = group
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("select[name=\"internal_group\"]").select_option(internal_group)
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("SELECT", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text(organization).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("region-search").get_by_text("Save").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"storeId\"]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"storeId\"]").fill(f"store_mask")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"enrollmentNumber\"]").fill(f"enroll_mask")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("spinbutton").fill(spinbutton_value)
    page.wait_for_timeout(delay)  # Explicit delay

    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    page.locator("input[name='timeIncident']").fill(current_time)
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("input[name=\"action\"]").fill(f"action_mask")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("SUBMIT REVIEW").click()
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator(".panel-div > .controller-panel-div > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def add_face_and_note_to_subject(page, delay):
    page.get_by_text("Enrollments").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("right-margin-menu > div:nth-child(2)").first.click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.locator("input[type='file']").set_input_files(conftest.FACE)
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@ng-click='skipCropping(); $event.stopPropagation();'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@ng-click='addPhoto(); $event.stopPropagation();'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@ng-mousedown='closeCurrentPanel(panel); $event.stopPropagation();'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[2]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("right-margin-menu > div:nth-child(3)").first.click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.locator(".right-margin-extended-button > .fa").first.click()
    # page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#Notes").get_by_text("Action", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Add A New Note To Person").click()
    page.wait_for_timeout(delay)  # Explicit delay
    # page.locator("input[type='file']").set_input_files(conftest.NOTE)
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@ng-click='skipCropping(); $event.stopPropagation();'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@ng-click='addImage(); $event.stopPropagation();'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("button", name="  Add Location").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Find Location").fill("bengakuru")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Kempegowda International").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("button", name="Kempegowda International").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@ng-click='closeCurrentPanel(panel);'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//a[normalize-space()='Save'])[1]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[3]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[2]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(".close-button-large").first.click()
    page.wait_for_timeout(delay)  # Explicit delay


def detect_face(page, image_file, delay):
    logger.info(f"Detect Face Subject: {image_file}")
    page.get_by_text("Detect Faces", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name='image']").first.set_input_files(image_file)
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path=f"screenshots/_17_detect_face_subject_uploaded.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(".select-areas-background-area").first.click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("i:nth-child(2)").first.click()
    page.wait_for_timeout(delay)  # Explicit delay
    with page.expect_download() as download_info:
        page.locator("right-margin-menu div").first.click()
        page.wait_for_timeout(delay)  # Explicit delay
    download = download_info.value
    download.save_as('screenshots/detect_face/' + download.suggested_filename)
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=(//div[@class='close-button-large posabs tac'])[2]").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(".close-button-large").first.click()
    page.wait_for_timeout(delay)  # Explicit delay


def configure_notifier(page, delay):
    page.get_by_text("Notifier", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#notifier-settings-button").nth(1).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("link", name="Collapse all").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("link", name="Expand all").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("link", name="Select all", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("link", name="Unselect all").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Search").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Search").fill("mxeast")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#tree-root div").filter(has_text="Kroger MX East - MXEAST").locator("i").nth(1).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("link", name="Save").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path="screenshots/_16_notifier_should_be_empty.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#notifier_1 div").filter(has_text="FACEFIRST Notifier Notifier").locator("i").first.click()
    page.wait_for_timeout(delay)  # Explicit delay


def generate_report(page, delay):
    page.locator("#reportField1Menu").select_option("string:number of events")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#reportField2MenuA").select_option("string:person")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#panel-container div").filter(has_text="Generate Report").nth(4).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path="screenshots/_17_reporting_number_of_probable_match_events_by_enrollment.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#chart_1 div").filter(has_text="Reporting").locator("div").click()
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("#reportField2MenuA").select_option("string:zone")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#panel-container div").filter(has_text="Generate Report").nth(4).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path="screenshots/_17_reporting_number_of_probable_match_events_by_zone.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#chart_2 div").filter(has_text="Reporting").locator("div").click()
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("#reportField1Menu").select_option("string:number of people")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#reportField2MenuC").select_option("string:zone")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#panel-container div").filter(has_text="Generate Report").nth(4).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path="screenshots/_17_reporting_number_of_enrollments_by_zone.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#chart_3 div").filter(has_text="Reporting").locator("div").click()
    page.wait_for_timeout(delay)  # Explicit delay

    page.locator("#reportField1Menu").select_option("string:number of zones")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#reportField2MenuB").select_option("string:person")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#panel-container div").filter(has_text="Generate Report").nth(4).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path="screenshots/_17_reporting_number_of_zones_by_enrollment.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("#chart_4 div").filter(has_text="Reporting").locator("div").click()
    page.wait_for_timeout(delay)  # Explicit delay


def update_enrollment_group(page, delay):
    page.get_by_text("Enrollment Groups").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("right-margin-menu > div:nth-child(4)").first.click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("a").filter(has_text="Action").nth(1).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Edit").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"faceThreshold\"]").clear()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"faceThreshold\"]").fill("0.87")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"maskedFaceThreshold\"]").clear()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("input[name=\"maskedFaceThreshold\"]").fill("0.87")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_text("Save", exact=True).click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.screenshot(path="screenshots/_18_enrollment_group_update_for_audit_log_report.png")
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(".panel-div > .controller-panel-div > .panel-heading-container > .close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator(".close-button-large").click()
    page.wait_for_timeout(delay)  # Explicit delay


def verify_dashboard_metrics(page1, delay):
    assert page1.locator("#LossPrevented-0").text_content() == "Total Loss Prevented$5,000"
    assert page1.locator("#ActiveEnrollments-0").text_content() == "Total New Enrollments26"
    assert page1.locator("#AllActiveEnrollmentsRegardlessOfTimeCreated-0").text_content() == ("Total FaceFirst "
                                                                                              "Enrollments26")
    assert page1.locator("#TotalMatchEvents-0").text_content() == "Total Probable Match Events25"
    assert page1.locator("#VisitorSearches-0").text_content() == "Visitor Searches11"
    assert page1.locator("#InvestigationSavingsTimeInHours-0").text_content() == "Investigation Savings Time (hours)88"
    assert page1.locator("#TotalIdentifiedEventLossValue-0").text_content() == "Total Identified Event Loss Value$5,000"
    assert page1.locator("#TotalActiveEnrollmentsReportedLoss-0").text_content() == ("Total Active Enrollments "
                                                                                     "Reported Loss$5,500")
    assert page1.locator("#RepeatPeopleOfInterest-0").text_content() == "Repeat People of Interest0"
    assert page1.locator("div:nth-child(10) > .ff--dynamic-widget__wrapper > .ant-card > .ant-card-body").text_content() == "Tag NameResponded Probable Match EventsDeterred Probable Match Eventsassualt55push cart55threat55"
    assert page1.locator("div:nth-child(11) > .ff--dynamic-widget__wrapper > .ant-card > .ant-card-body").text_content() == "Enrollment GroupTotal Probable Match EventsResponded Probable Match EventsDeterred Probable Match Eventsabe555pte555soe555"
    page1.screenshot(path="screenshots/_19_insight_dashboard_overview.png")
    page1.wait_for_timeout(delay)  # Explicit delay


def verify_event_dashboard_matrices(page1, delay):
    page1.get_by_role("button", name="Overview Dashboard caret-down").click()
    page1.wait_for_timeout(delay)  # Explicit delay
    page1.get_by_text("Probable Match Events Dashboard").click()
    page1.wait_for_timeout(delay)  # Explicit delay

    assert page1.locator("#deterred-events").text_content() == "Deterred Probable Match Events25"
    assert page1.locator("#TotalTaggedEvents-0").text_content() == "Total Tagged Probable Match Events25"
    assert page1.locator(
        "#SeriousOffenderTaggedEvents-0").text_content() == "Serious Offender Tagged Probable Match Events15"
    assert page1.locator("#TotalMatchEvents-0").text_content() == "Total Probable Match Events25"
    page1.screenshot(path="screenshots/_20_insight_dashboard_events_1_.png")
    page1.wait_for_timeout(delay)  # Explicit delay

    with page1.expect_popup() as page2_info:
        page1.locator(
            "div:nth-child(14) > div > .ant-card > .ant-card-body > div > .echarts-for-react > div > canvas").click(
            position={"x": 694, "y": 104})
    page1.wait_for_timeout(delay)  # Explicit delay
    page1.screenshot(path="screenshots/_20_insight_dashboard_events_2_.png")
    page2 = page2_info.value
    page2.wait_for_timeout(delay)  # Explicit delay
    page2.screenshot(path="screenshots/_20_insight_dashboard_events_3_.png")
    page2.wait_for_timeout(delay)  # Explicit delay

    try:
        page2.close()
    except Exception as e:
        logger.error(f"An error occurred during Insight dashboard overview report: {e}")
        page2.screenshot(path="screenshots/_20_insight_dashboard_events_closing_error_1_.png")

    page1.wait_for_timeout(delay)  # Explicit delay

    try:
        page1.close()
    except Exception as e:
        logger.error(f"An error occurred during Insight dashboard overview report: {e}")
        page1.screenshot(path="screenshots/_20_insight_dashboard_events_closing_error_2_.png")


def verify_enrollment_dashboard_metrics(page1, delay):
    page1.get_by_role("button", name="Overview Dashboard caret-down").click()
    page1.wait_for_timeout(delay)  # Explicit delay
    page1.get_by_text("Enrollments Dashboard").click()
    page1.wait_for_timeout(delay)  # Explicit delay

    assert page1.locator(".ff--scorecard").first.text_content() == "Total New Enrollments26"
    assert page1.locator(".ff--scorecard").nth(1).text_content() == "Total FaceFirst Enrollments26"
    page1.screenshot(path="screenshots/_21_insight_dashboard_enrollment_1_.png")
    page1.wait_for_timeout(delay)  # Explicit delay

    try:
        page1.close()
    except Exception as e:
        logger.error(f"An error occurred during Insight dashboard enrollment report: {e}")
        page1.screenshot(path="screenshots/_21_insight_dashboard_enrollment_closing_error.png")


def welcome(page, delay):
    try:
        logger.info("Welcome to the FaceFirst Platform.")
        page.get_by_role("button", name="Close").click()
        logger.info("Clicked the Close button.")
        page.wait_for_timeout(delay)  # Explicit delay
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def dm_log_in(page, credentials, delay):
    page.get_by_role("textbox", name="Email (Username) *").fill(credentials["email"])
    logger.info("Filled out the Email field for login.")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("textbox", name="Password *").fill(credentials["password"])
    logger.info("Filled out the Password field for login.")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("button", name="Login").click()
    logger.info("Clicked the Login button.")
    page.wait_for_timeout(delay)  # Explicit delay
    logger.info(f"login_user:{credentials["email"]}")


def dm_log_out(page, delay):
    page.wait_for_timeout(delay)  # Explicit delay
    page.locator("xpath=/html[1]/body[1]/div[1]/div[1]/header[1]/div[1]/div[2]/a[1]").click()
    logger.info("Clicked the core link.")
    page.wait_for_timeout(delay)  # Explicit delay
    page.get_by_role("menuitem", name="Logout").click()
    logger.info("Clicked the Logout menu item.")
    page.wait_for_timeout(delay)  # Explicit delay


def create_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    report_file = report_dir / f"report_{timestamp}.html"

    pytest.main([
        f"--html={report_file}",
        "--self-contained-html"
    ])

