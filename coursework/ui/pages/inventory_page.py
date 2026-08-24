import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from ui.pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    BURGER_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.CSS_SELECTOR, "[data-test='logout-sidebar-link']")
    RESET_LINK = (By.CSS_SELECTOR, "[data-test='reset-sidebar-link']")

    @staticmethod
    def _product_slug(product_name: str) -> str:
        return product_name.lower().replace(" ", "-")

    def _add_button(self, product_name: str) -> tuple[str, str]:
        return (By.CSS_SELECTOR, f"[data-test='add-to-cart-{self._product_slug(product_name)}']")

    def _remove_button(self, product_name: str) -> tuple[str, str]:
        return (By.CSS_SELECTOR, f"[data-test='remove-{self._product_slug(product_name)}']")

    def _item_name_link(self, product_name: str) -> tuple[str, str]:
        return (
            By.XPATH,
            f"//div[@data-test='inventory-item-name' and text()='{product_name}']",
        )

    @allure.step("Wait until inventory page is loaded")
    def wait_loaded(self) -> None:
        self.wait_visible(self.INVENTORY_CONTAINER)

    @allure.step("Add product to cart: {product_name}")
    def add_to_cart(self, product_name: str) -> None:
        self.click(self._add_button(product_name))

    @allure.step("Remove product from inventory: {product_name}")
    def remove_from_inventory(self, product_name: str) -> None:
        self.click(self._remove_button(product_name))

    @allure.step("Open product details: {product_name}")
    def open_product(self, product_name: str) -> None:
        self.click(self._item_name_link(product_name))

    @allure.step("Open cart")
    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    @allure.step("Get cart badge count")
    def cart_count(self) -> int:
        badges = self.find_all(self.CART_BADGE)
        if not badges:
            return 0
        return int(badges[0].text)

    @allure.step("Get product names")
    def get_product_names(self) -> list[str]:
        return self.get_elements_text(self.ITEM_NAME)

    @allure.step("Get product prices")
    def get_product_prices(self) -> list[float]:
        raw_prices = self.get_elements_text(self.ITEM_PRICE)
        return [float(price.replace("$", "")) for price in raw_prices]

    def get_product_price(self, product_name: str) -> str:
        names = self.get_product_names()
        prices = self.get_elements_text(self.ITEM_PRICE)
        return prices[names.index(product_name)]

    @allure.step("Sort products by '{value}'")
    def sort_by(self, value: str) -> None:
        dropdown = Select(self.wait_visible(self.SORT_DROPDOWN))
        dropdown.select_by_value(value)
        self.wait_until(
            lambda d: Select(d.find_element(*self.SORT_DROPDOWN)).first_selected_option.get_attribute("value")
            == value
        )

    @allure.step("Open burger menu")
    def open_menu(self) -> None:
        self.click(self.BURGER_BUTTON)
        self.wait_visible(self.LOGOUT_LINK)

    @allure.step("Log out")
    def logout(self) -> None:
        self.open_menu()
        self.click(self.LOGOUT_LINK)
