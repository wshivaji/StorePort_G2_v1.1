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


        #above columns like search on store,filter by event time,filter by classification
    def click_on_store(self):
        self.page.get_by_role("textbox", name="Search by Store Name").click()
        self.page.get_by_role("textbox", name="Search by Store Name").press("CapsLock")
        self.page.get_by_role("textbox", name="Search by Store Name").fill("SAFEWAY 1804")
        self.page.get_by_role("textbox", name="Search by Store Name").press("Enter")
        self.page.get_by_role("textbox", name="Filter By Event Time in Store").click()
        self.page.locator("div").filter(has_text=re.compile(r"^Filter By Event Time in Store$")).get_by_role(
            "button").click()
        self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).first.click()
        self.page.get_by_role("button", name="31").click()
        self.page.get_by_role("button", name="31").press("Enter")
        self.page.locator(".MuiSelect-select").first.click()
        self.page.get_by_role("option", name="Confirmed", exact=True).get_by_role("paragraph").click()
        self.page.get_by_role("option", name="No filters applied").press("Enter")
        self.page.get_by_role("option", name="Confirmed", exact=True).get_by_role("paragraph").click()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(1).click()


    def validate_filtered_store_data(self):
        # Applying the filter for "Store" column with value "SAFEWAY 1804"
        self.page.locator("div").filter(has_text=re.compile(r"^Store$")).nth(2).click()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(2).hover()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(2).click()
        self.page.get_by_role("menuitem", name="Filters").click()
        self.page.locator("div").filter(has_text=re.compile(r"^Value$")).click()
        self.page.get_by_role("textbox", name="Value").press("CapsLock")
        self.page.get_by_role("textbox", name="Value").fill("SAFEWAY 1804")
        self.page.get_by_role("button", name="APPLY FILTER").click()
        self.page.wait_for_timeout(3000)
        assert  self.page.locator("div:nth-child(2) > div:nth-child(2) > .MuiStack-root > .MuiBox-root > span > .MuiTypography-root").inner_text()

    def Ammount(self):
        self.page.get_by_text("Amount").click()
        self.page.get_by_role("row", name="Event Time in Store Store").get_by_role("button").nth(1).click()
        amount_values = []
        # Locate the 'Amount' column specifically and extract the values
        rows = self.page.locator("table tbody tr")
        for row in rows.all():
            amount = row.locator('td:nth-child(5)').text_content()
            if amount:
                try:
                    amount_values.append(float(amount.strip()))
                except ValueError:
                    continue
        # Check if the list is in ascending order
        is_sorted = all(amount_values[i] <= amount_values[i + 1] for i in range(len(amount_values) - 1))
        assert is_sorted


































