import allure
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish']")
    TOTAL_LABEL = (By.CSS_SELECTOR, "[data-test='total-label']")

    @allure.step("Wait until checkout overview is loaded")
    def wait_loaded(self) -> None:
        self.wait_visible(self.FINISH_BUTTON)

    @allure.step("Get overview item names")
    def get_item_names(self) -> list[str]:
        return self.get_elements_text(self.ITEM_NAME)

    @allure.step("Finish checkout")
    def finish(self) -> None:
        self.click(self.FINISH_BUTTON)
