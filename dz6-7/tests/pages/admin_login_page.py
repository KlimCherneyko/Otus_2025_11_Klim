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
    DASHBOARD_HEADER = (By.CSS_SELECTOR, ".page-header h1")

    def open(self) -> None:
        super().open("admin/")

    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def wait_for_dashboard(self) -> None:
        self.wait_until(ec.any_of(ec.visibility_of_element_located(self.LOGOUT_LINK), ec.url_contains("dashboard")))

    def get_user_token(self) -> str:
        query = urlparse(self.driver.current_url).query
        return parse_qs(query).get("user_token", [""])[0]

    def logout(self) -> None:
        self.click(self.LOGOUT_LINK)
