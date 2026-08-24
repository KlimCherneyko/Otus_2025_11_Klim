import allure
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    TEXT = (By.CSS_SELECTOR, "[data-test='complete-text']")
    BACK_HOME = (By.CSS_SELECTOR, "[data-test='back-to-products']")

    @allure.step("Wait until checkout complete page is loaded")
    def wait_loaded(self) -> None:
        self.wait_visible(self.HEADER)

    @allure.step("Get complete header")
    def get_header(self) -> str:
        return self.get_text(self.HEADER)
