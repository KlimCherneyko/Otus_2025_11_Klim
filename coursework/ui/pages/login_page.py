import allure
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    @allure.step("Open login page")
    def open(self, path: str = "") -> None:
        super().open(path)

    @allure.step("Log in as '{username}'")
    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Get login error message")
    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self.ERROR_MESSAGE)
