import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from tests.pages.base_page import BasePage


class RegistrationPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "#content h1")
    FIRST_NAME_INPUT = (By.ID, "input-firstname")
    LAST_NAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    TELEPHONE_INPUT = (By.ID, "input-telephone")
    PASSWORD_INPUT = (By.ID, "input-password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "input-confirm")
    AGREE_CHECKBOX = (By.NAME, "agree")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[type='submit'][value='Continue']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content p")
    SUCCESS_URL_PART = "account/success"

    @allure.step("Open registration page")
    def open(self) -> None:
        super().open("index.php?route=account/register")

    @allure.step("Register new customer: {email}")
    def register(self, first_name: str, last_name: str, email: str, telephone: str, password: str) -> None:
        self.logger.info("Registering customer: %s %s <%s>", first_name, last_name, email)
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.TELEPHONE_INPUT, telephone)
        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, password)
        self.click(self.AGREE_CHECKBOX)
        self.click(self.CONTINUE_BUTTON)

    @allure.step("Wait for registration success")
    def wait_for_success(self) -> str:
        self.logger.info("Waiting for registration success page")
        self.wait_until(ec.url_contains(self.SUCCESS_URL_PART))
        message = self.wait_visible(self.SUCCESS_MESSAGE).text.strip()
        self.logger.info("Registration success message: %s", message)
        return message
