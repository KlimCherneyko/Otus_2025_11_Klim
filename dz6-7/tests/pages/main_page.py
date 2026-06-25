from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from tests.pages.base_page import BasePage


class MainPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "#logo a")
    SEARCH_INPUT = (By.NAME, "search")
    NAVBAR_MENU = (By.ID, "menu")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "#content .product-thumb")
    PRICE_VALUES = (By.CSS_SELECTOR, "#content .product-thumb .price")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".caption a")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[onclick*='cart.add']")
    CART_BUTTON = (By.ID, "cart-total")
    CART_PAGE_ITEMS = (By.CSS_SELECTOR, "#content .table-responsive td.text-left a")

    def open(self) -> None:
        super().open("")
        self._wait_for_featured_products()

    def _wait_for_featured_products(self) -> None:
        self.wait_until(lambda d: len(d.find_elements(*self.PRODUCT_CARDS)) > 0, timeout=20)

    def get_prices_text(self) -> list[str]:
        self._wait_for_featured_products()
        return [price.text.strip() for price in self.driver.find_elements(*self.PRICE_VALUES) if price.text.strip()]

    def _cart_total_text(self) -> str:
        try:
            return self.driver.find_element(*self.CART_BUTTON).text.strip()
        except StaleElementReferenceException:
            return ""

    def _product_cards(self) -> list:
        return self.driver.find_elements(*self.PRODUCT_CARDS)

    def add_first_product_to_cart(self) -> str:
        cards = self._product_cards()
        if not cards:
            raise AssertionError("No featured products on main page")

        card = cards[0]
        cart_total_before = self._cart_total_text()
        product_name = card.find_element(*self.PRODUCT_NAME).text.strip()
        card.find_element(*self.ADD_TO_CART_BUTTON).click()

        self.wait_until(
            lambda d: self._cart_total_text() not in ("", cart_total_before),
            timeout=6,
        )
        return product_name

    def open_cart_page(self) -> None:
        super().open("index.php?route=checkout/cart")

    def cart_page_items(self) -> list[str]:
        self.wait_until(lambda d: len(d.find_elements(*self.CART_PAGE_ITEMS)) > 0)
        return [item.text.strip() for item in self.driver.find_elements(*self.CART_PAGE_ITEMS) if item.text.strip()]
