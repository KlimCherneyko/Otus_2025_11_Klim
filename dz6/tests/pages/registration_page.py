from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class RegistrationPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "#content h1")
    FIRST_NAME_INPUT = (By.ID, "input-firstname")
    LAST_NAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    AGREE_CHECKBOX = (By.NAME, "agree")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[type='submit'][value='Continue']")
    RIGHT_COLUMN = (By.ID, "column-right")

    def open(self) -> None:
        super().open("index.php?route=account/register")
