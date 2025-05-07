import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from PageObjects.LoginPage import LoginPage
from PageObjects.DashboardPage import DashboardPage
from Utilities.config import Config


class TestLogoutFunctionality:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(Config.BASE_URL)

       
        login = LoginPage(self.driver)
        login.enter_username(Config.USERNAME)
        login.enter_password(Config.PASSWORD)
        login.click_login()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )

        yield
        self.driver.quit()

    def test_user_can_logout_successfully(self):
        dashboard = DashboardPage(self.driver)
        dashboard.click_user_dropdown()
        dashboard.click_logout()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[1]/img'))
        )

        login = LoginPage(self.driver)
        assert "OrangeHRM" in login.get_login_page_title(), "User was not redirected to login page after logout"

        
        if not os.path.exists("Screenshots"):
            os.makedirs("Screenshots")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"Screenshots/test_logout_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)
