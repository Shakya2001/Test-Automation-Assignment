import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjects.LoginPage import LoginPage
from PageObjects.DashboardPage import DashboardPage
from PageObjects.LeavePage import LeavePage
from Utilities.config import Config


class TestLeave:
    """Test class for leave functionality testing"""

    @pytest.fixture(scope="class")
    def driver(self):
        """Fixture to initialize and quit the WebDriver"""
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()

    @pytest.fixture(scope="function")
    def authenticated_driver(self, driver):
        """Fixture to handle login and authentication before each test"""
        driver.get(Config.BASE_URL)

       
        login_page = LoginPage(driver)
        login_page.enter_username(Config.USERNAME)
        login_page.enter_password(Config.PASSWORD)
        login_page.click_login()

        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//h6[text()="Dashboard"]'))
        )

        return driver

    def test_leave_page_navigation(self, authenticated_driver):
        """Test navigation to leave page and verify header"""
        
        dashboard_page = DashboardPage(authenticated_driver)
        dashboard_page.click_my_leave()

        
        WebDriverWait(authenticated_driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "oxd-layout")]'))
        )

       
        leave_page = LeavePage(authenticated_driver)
        header_text = leave_page.get_leave_header()

        
        assert header_text, "No header text found - leave page element not located"
        assert any(phrase in header_text for phrase in ["My Leave", "Leave List", "Leave"]), \
            f"Expected leave-related header but got: '{header_text}'"

        
        if not os.path.exists("Screenshots"):
            os.makedirs("Screenshots")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"Screenshots/test_leave_{timestamp}.png"
        authenticated_driver.save_screenshot(screenshot_path)
