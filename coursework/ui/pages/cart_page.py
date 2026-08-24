import allure
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    CART_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, "[data-test='continue-shopping']")

    @staticmethod
    def _product_slug(product_name: str) -> str:
        return product_name.lower().replace(" ", "-")

    def _remove_button(self, product_name: str) -> tuple[str, str]:
        return (By.CSS_SELECTOR, f"[data-test='remove-{self._product_slug(product_name)}']")

    @allure.step("Wait until cart page is loaded")
    def wait_loaded(self) -> None:
        self.wait_visible(self.TITLE)

    @allure.step("Get cart item names")
    def get_item_names(self) -> list[str]:
        return [element.text for element in self.find_all(self.ITEM_NAME)]

    @allure.step("Remove product from cart: {product_name}")
    def remove_item(self, product_name: str) -> None:
        self.click(self._remove_button(product_name))

    @allure.step("Proceed to checkout")
    def checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    def items_count(self) -> int:
        return len(self.find_all(self.CART_ITEM))
