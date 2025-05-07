import os
from datetime import datetime
import pytest
from selenium import webdriver

from PageObjects.LoginPage import LoginPage
from Utilities.config import Config


class TestHomePageTitle:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(Config.BASE_URL)
        yield
        self.driver.quit()

    def test_verify_home_page_title(self):
        login_page = LoginPage(self.driver)
        actual_title = login_page.get_login_page_title()
        expected_title = "OrangeHRM"

        assert actual_title == expected_title, \
            f"Expected title to be '{expected_title}' but got '{actual_title}'"

       
        if not os.path.exists("Screenshots"):
            os.makedirs("Screenshots")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"Screenshots/test_title_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)
