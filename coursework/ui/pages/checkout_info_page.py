import allure
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")

    @allure.step("Wait until checkout info page is loaded")
    def wait_loaded(self) -> None:
        self.wait_visible(self.FIRST_NAME)

    @allure.step("Fill checkout info: {first_name} {last_name}, {postal_code}")
    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)

    @allure.step("Continue to overview")
    def continue_checkout(self) -> None:
        self.click(self.CONTINUE_BUTTON)

    @allure.step("Submit checkout info")
    def submit(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill_info(first_name, last_name, postal_code)
        self.continue_checkout()

    @allure.step("Get checkout validation error")
    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
