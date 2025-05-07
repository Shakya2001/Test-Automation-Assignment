import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjects.LoginPage import LoginPage
from PageObjects.DashboardPage import DashboardPage
from Utilities.config import Config


class TestLoginFunctionality:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(Config.BASE_URL)
        yield
        self.driver.quit()

    def test_valid_login_redirects_to_dashboard(self):
        # Login to the application
        login = LoginPage(self.driver)
        login.enter_username(Config.USERNAME)
        login.enter_password(Config.PASSWORD)
        login.click_login()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )

        dashboard = DashboardPage(self.driver)
        header_text = dashboard.get_dashboard_header()

        assert header_text == "Dashboard", f"Expected 'Dashboard' but got '{header_text}'"
