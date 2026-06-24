import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from tests.pages.base_page import BasePage


class MainPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "#logo a")
    SEARCH_INPUT = (By.NAME, "search")
    NAVBAR_MENU = (By.ID, "menu")
    FOOTER = (By.TAG_NAME, "footer")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "#content .product-thumb")
    PRICE_VALUES = (By.CSS_SELECTOR, "#content .product-thumb .price")
    CURRENCY_BUTTON = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    CART_BUTTON = (By.ID, "cart-total")
    CART_ITEMS = (By.CSS_SELECTOR, "#cart .dropdown-menu .table td.text-left a, #cart .dropdown-menu .table .text-left a")
    CART_PAGE_ITEMS = (By.CSS_SELECTOR, "#content .table-responsive td.text-left a")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")

    def open(self) -> None:
        super().open("")
        self._wait_for_featured_products()

    def _wait_for_featured_products(self) -> None:
        self.wait_until(lambda d: len(d.find_elements(*self.PRODUCT_CARDS)) > 0, timeout=20)

    def switch_currency(self, currency_title: str) -> None:
        self.click(self.CURRENCY_BUTTON)
        currency_locator = (
            By.XPATH,
            f"//form[@id='form-currency']//button[contains(normalize-space(), '{currency_title}')]",
        )
        self.click(currency_locator)

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

    def add_random_product_to_cart(self) -> str:
        cards_count = len(self._product_cards())
        indexes = list(range(cards_count))
        random.shuffle(indexes)

        for index in indexes:
            cards = self._product_cards()
            if index >= len(cards):
                continue
            card = cards[index]
            cart_total_before = self._cart_total_text()
            product_name = card.find_element(By.CSS_SELECTOR, ".caption a").text.strip()
            card.find_element(By.CSS_SELECTOR, "button[onclick*='cart.add']").click()

            try:
                self.wait_until(
                    lambda d: (
                        self._cart_total_text() not in ("", cart_total_before)
                        or len(self.driver.find_elements(By.CSS_SELECTOR, ".alert-danger")) > 0
                    ),
                    timeout=6,
                )
            except TimeoutException:
                continue

            if self._cart_total_text() not in ("", cart_total_before):
                return product_name

        raise AssertionError("Could not add any featured product to cart")

    def open_cart_dropdown(self) -> None:
        self.click(self.CART_BUTTON)

    def cart_items(self) -> list[str]:
        self.wait_until(lambda d: len(d.find_elements(*self.CART_ITEMS)) > 0)
        return [item.text.strip() for item in self.driver.find_elements(*self.CART_ITEMS) if item.text.strip()]

    def open_cart_page(self) -> None:
        super().open("index.php?route=checkout/cart")

    def cart_page_items(self) -> list[str]:
        self.wait_until(lambda d: len(d.find_elements(*self.CART_PAGE_ITEMS)) > 0)
        return [item.text.strip() for item in self.driver.find_elements(*self.CART_PAGE_ITEMS) if item.text.strip()]
