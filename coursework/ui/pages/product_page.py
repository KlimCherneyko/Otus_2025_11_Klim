import allure
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class ProductPage(BasePage):
    NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    DESCRIPTION = (By.CSS_SELECTOR, "[data-test='inventory-item-desc']")
    BACK_BUTTON = (By.CSS_SELECTOR, "[data-test='back-to-products']")
    ADD_TO_CART = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")

    @allure.step("Wait until product page is loaded")
    def wait_loaded(self) -> None:
        self.wait_visible(self.NAME)

    @allure.step("Get product name from details page")
    def get_name(self) -> str:
        return self.get_text(self.NAME)

    @allure.step("Get product price from details page")
    def get_price(self) -> str:
        return self.get_text(self.PRICE)

    @allure.step("Add product to cart from details page")
    def add_to_cart(self) -> None:
        self.click(self.ADD_TO_CART)

    @allure.step("Go back to inventory")
    def back_to_products(self) -> None:
        self.click(self.BACK_BUTTON)
