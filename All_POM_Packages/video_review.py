from playwright.sync_api import sync_playwright
import re

class VideoReview:
    def __init__(self, page):
        try:
            self.page = page
        except Exception as ex:
            print(f"Error in initializing UserCreation: {type(ex).__name__} ")
    def  click_video_review_config(self):
        self.page.locator('//span[text()="Video Review"]').click()


    # def click_on_store(self):
    #     self.page.get_by_role("textbox", name="Search by Store Name").click()
    #     self.page.get_by_role("textbox", name="Search by Store Name").press("CapsLock")
    #     self.page.get_by_role("textbox", name="Search by Store Name").fill("SAFEWAY 1804")
    #     self.page.get_by_role("textbox", name="Search by Store Name").press("Enter")
    #     self.page.get_by_role("textbox", name="Filter By Event Time in Store").click()
    #     self.page.locator("div").filter(has_text=re.compile(r"^Filter By Event Time in Store$")).get_by_role(
    #         "button").click()
    #     self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).first.click()
    #     self.page.get_by_role("button", name="31").click()
    #     self.page.get_by_role("button", name="31").press("Enter")
    #     self.page.locator(".MuiSelect-select").first.click()
    #     self.page.get_by_role("option", name="Confirmed", exact=True).get_by_role("paragraph").click()
    #     self.page.get_by_role("option", name="No filters applied").press("Enter")
    #     self.page.get_by_role("option", name="Confirmed", exact=True).get_by_role("paragraph").click()
    #     self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(1).click()


    def click_on_ascending(self):


        #clicking on store
        self.page.locator("div").filter(has_text=re.compile(r"^Store$")).nth(2).click()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(2).hover()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(2).click()
        self.page.get_by_role("menuitem", name="Filters").click()
        self.page.locator("div").filter(has_text=re.compile(r"^Value$")).click()
        self.page.get_by_role("textbox", name="Value").press("CapsLock")
        self.page.get_by_role("textbox", name="Value").fill("SAFEWAY 1804")
        self.page.get_by_role("button", name="APPLY FILTER").click()


        # click on exit location
        self.page.locator("div").filter(has_text=re.compile(r"^Exit Location$")).nth(1).click()
        self.page.locator(".MuiPopover-root.MuiMenu-root.MuiModal-root.css-1sucic7 > .MuiBackdrop-root").click()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(2).hover()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(2).click()
        self.page.get_by_role("menuitem", name="Filters").click()
        self.page.get_by_role("textbox", name="Value").nth(1).click()
        self.page.get_by_role("textbox", name="Value").nth(1).fill("STARBUCKS DOOR")
        self.page.get_by_role("button", name="APPLY FILTER").click()



        # click on 30d theft activity
        self.page.locator("div").filter(has_text=re.compile(r"^30d Theft Activity$")).nth(1).click()
        self.page.locator(".MuiPopover-root.MuiMenu-root.MuiModal-root.css-1sucic7 > .MuiBackdrop-root").click()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(1).hover()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(1).click()
        self.page.get_by_role("menuitem", name="Filters").click()
        self.page.locator(
            ".MuiInputBase-root.MuiOutlinedInput-root.MuiInputBase-colorPrimary.MuiInputBase-formControl.MuiInputBase-sizeSmall.css-1w52ef5 > .MuiSelect-select").click()
        self.page.get_by_role("option", name="Typical").click()
        self.page.locator("#menu- div").first.click()
        self.page.get_by_role("button", name="APPLY FILTER").click()

















