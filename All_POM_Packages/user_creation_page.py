from playwright.sync_api import Page
from conftest import *


class UserCreation:
    def __init__(self, page):
        try:
            self.page = page
        except Exception as ex:
            print(f"Error in initializing UserCreation: {type(ex).__name__} ")

    def click_user_management(self):
        try:
            self.page.locator('//span[text()="User Management"]').click()
        except Exception as ex:
            print(f"Error in click_user_management: {type(ex).__name__} ")

    def click_on_add_user(self):
        try:
            self.page.locator('//span//child::button[@class="MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeSmall css-15nnysv"]').click()
        except Exception as ex:
            print(f"Error in click_on_add_user: {type(ex).__name__} ")

    def fill_first_name(self):
        try:
            self.page.fill('//input[@name="firstName"]', "sinchu")
        except Exception as ex:
            print(f"Error in fill_first_name: {type(ex).__name__} ")

    def fill_last_name(self):
        try:
            self.page.fill('//input[@name="lastName"]', "devanapalli")
        except Exception as ex:
            print(f"Error in fill_last_name: {type(ex).__name__} ")

    def fill_email(self):
        try:
            self.page.fill('//input[@name="email"]', 's60191821@gmail.com')
        except Exception as ex:
            print(f"Error in fill_email: {type(ex).__name__} ")

    def fill_company(self):
        try:
            self.page.get_by_role("combobox").first.click()
            self.page.get_by_role("option", name="Gatekeeper").click()
        except Exception as ex:
            print(f"Error in fill_company: {type(ex).__name__}")

    def fill_country(self):
        try:
            self.page.get_by_role("combobox").nth(1).click()
            self.page.get_by_role("option", name="Austria").click()
        except Exception as ex:
            print(f"Error in fill_country: {type(ex).__name__} ")

    def fill_role(self):
        try:
            self.page.get_by_role("combobox").nth(2).click()
            self.page.get_by_role("option", name="Admin - Full", exact=True).click()
        except Exception as ex:
            print(f"Error in fill_role: {type(ex).__name__} ")

    def clicking_on_save(self):
        try:
            self.page.locator('//button[text()="Save"]').click()
        except Exception as ex:
            print(f"Error in clicking_on_save: {type(ex).__name__} ")
