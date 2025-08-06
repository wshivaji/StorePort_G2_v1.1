class MainPage:
    def __init__(self, page):
        self.page = page

    def click_user_management(self):
        self.page.click('//span[text()="User Management"]')
        


