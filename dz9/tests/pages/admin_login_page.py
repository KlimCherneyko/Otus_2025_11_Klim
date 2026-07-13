import allure
from urllib.parse import parse_qs, urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from tests.pages.base_page import BasePage


class AdminLoginPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, ".panel-title")
    USERNAME_INPUT = (By.ID, "input-username")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOTTEN_PASSWORD_LINK = (By.CSS_SELECTOR, ".help-block a")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href*='common/logout']")

    @allure.step("Open admin login page")
    def open(self) -> None:
        super().open("admin/")

    @allure.step("Login to admin panel")
    def login(self, username: str, password: str) -> None:
        self.logger.info("Logging in as admin user: %s", username)
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Wait for admin dashboard")
    def wait_for_dashboard(self) -> None:
        self.logger.info("Waiting for admin dashboard")
        self.wait_until(ec.any_of(ec.visibility_of_element_located(self.LOGOUT_LINK), ec.url_contains("dashboard")))

    @allure.step("Get admin user token")
    def get_user_token(self) -> str:
        query = urlparse(self.driver.current_url).query
        token = parse_qs(query).get("user_token", [""])[0]
        self.logger.info("Retrieved user token")
        return token

    @allure.step("Logout from admin panel")
    def logout(self) -> None:
        self.logger.info("Logging out from admin panel")
        self.click(self.LOGOUT_LINK)

    @allure.step("Wait for admin login page")
    def wait_for_login_page(self) -> None:
        self.logger.info("Waiting for admin login page")
        self.wait_until(ec.url_contains("common/login"))
        self.wait_visible(self.LOGIN_BUTTON)
        self.wait_visible(self.PAGE_TITLE)
